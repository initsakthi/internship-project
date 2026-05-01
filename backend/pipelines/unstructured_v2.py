import os
import asyncio
from processing import stream_loader, cleaner, chunker
from filtering import pre_filter
from validation import validator

#  Import from your modular AI service folder
from ai_services.local_llm import call_local_llm, extract_json

async def run_pipeline(file_path: str, tags: list):
    """
    Orchestrates the modular unstructured extraction flow.
    Uses LOCAL LLM (Ollama) and tracks page numbers for metadata.
    """
    all_extracted_records = []
    
    # 1. STREAM: Load text page-by-page
    pages = stream_loader.get_pages(file_path)

    # Use enumerate starting at 1 to track real-world page numbers
    for page_num, page_text in enumerate(pages, start=1):
        
        # 2. CLEAN: Normalize text for the specific page
        normalized_text = cleaner.normalize(page_text)
        
        # 3. CHUNK: Split into segments (smaller size for local LLM speed)
        text_chunks = chunker.split_by_tokens(normalized_text, chunk_size=1000)

        for chunk_index, chunk in enumerate(text_chunks):
            # 4. PRE-FILTER: Save compute by skipping irrelevant text
            if not pre_filter.is_relevant(chunk, tags):
                print(f"Skipping irrelevant chunk {chunk_index} on Page {page_num}")
                continue

            print(f" Calling LOCAL LLM (Gemma) for chunk {chunk_index} on Page {page_num}...")

            # 5. Build strict extraction prompt
            prompt = f"""
            SYSTEM: You are a JSON extraction API. Output ONLY valid JSON.
            USER: Extract these fields: {", ".join(tags)}
            
            TEXT TO ANALYZE:
            {chunk}

            JSON OUTPUT:
            """

            try:
                # 6. ASYNC LOCAL LLM CALL
                raw_output = await call_local_llm(prompt)
                parsed_data = extract_json(raw_output)
                
                print(f"Page {page_num} Response: {parsed_data}")

            except Exception as e:
                print(f" Local LLM Error on Page {page_num}: {e}")
                continue

            # 7. VALIDATION & FORMATTING
            if parsed_data and isinstance(parsed_data, dict):
                # Validate the dictionary and get confidence score
                validated_data, confidence = validator.validate_extraction(parsed_data)

                if validated_data:
                    # Flatten the data to match your Angular ExtractionRecord model
                    for tag, value in validated_data.items():
                        # Only add records if a real value was found
                        if value and str(value).lower() not in ["none", "null", "n/a"]:
                            record = {
                                "tag": tag,
                                "value": str(value),
                                "confidence_score": confidence,
                                "sourceFile": os.path.basename(file_path),
                                "page_number": page_num  
                            }
                            all_extracted_records.append(record)
                            print(f" Found on Page {page_num}: {tag} = {value}")

    # 8. FINAL RESPONSE
    print(f" Extraction Complete. Total records found: {len(all_extracted_records)}")
    
    return {
        "status": "success",
        "records": all_extracted_records
    }