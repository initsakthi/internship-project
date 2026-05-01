import spacy
import os
from extractors import extract_text
from patterns import extract_emails, extract_phones, extract_urls, extract_dates
from tag_mapper import map_tags_to_values

# Load model globally to prevent reloading on every request
print("Initializing AI Engine...")
try:
    nlp = spacy.load("en_core_web_lg")
except Exception:
    # Fallback to smaller model if large is missing to prevent hang
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        raise Exception("No SpaCy model found. Run: python -m spacy download en_core_web_sm")

def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    lines = [l.strip() for l in text.split("\n")]
    cleaned = []
    for line in lines:
        if line:
            cleaned.append(line)
        elif cleaned and cleaned[-1] != "":
            cleaned.append("")
    return "\n".join(cleaned).strip()

def process_document(file_path: str, user_tags: list) -> dict:
    # 1. Check if file actually exists
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}

    print(f"Processing: {os.path.basename(file_path)}")
    
    # 2. Extract text from pages
    try:
        pages = extract_text(file_path)
    except Exception as e:
        return {"status": "error", "message": f"Extraction Error: {str(e)}"}

    if not pages:
        return {"status": "error", "message": "Document is empty or unreadable"}

    aggregated_results = {}

    for page_data in pages:
        page_number = page_data["page"]
        raw_text = page_data["text"]

        if not raw_text or not raw_text.strip():
            continue

        cleaned_text = clean_text(raw_text)
        
        # AI Processing
        doc = nlp(cleaned_text)

        ner_entities = {}
        for ent in doc.ents:
            ner_entities.setdefault(ent.label_, [])
            if ent.text not in ner_entities[ent.label_]:
                ner_entities[ent.label_].append(ent.text)

        patterns = {
            "email": extract_emails(cleaned_text),
            "phone": extract_phones(cleaned_text),
            "url": extract_urls(cleaned_text),
            "date": extract_dates(cleaned_text)
        }

        # Map findings to user requested tags
        extracted = map_tags_to_values(
            user_tags=user_tags,
            ner_entities=ner_entities,
            patterns=patterns,
            full_text=cleaned_text
        )

        for tag, value in extracted.items():
            if not value or value == "Not found":
                continue

            if tag not in aggregated_results:
                aggregated_results[tag] = {
                    "value": value,
                    "pages": [page_number]
                }
            else:
                # Prevent duplicate page entries
                if page_number not in aggregated_results[tag]["pages"]:
                    aggregated_results[tag]["pages"].append(page_number)

    # 3. Return structured response for Angular table
    return {
        "status": "success",
        "extracted_data": aggregated_results
    }