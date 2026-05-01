def is_relevant(chunk: str, tags: list) -> bool:
    """Checks if any requested tags (or related keywords) exist in the chunk."""
    chunk_lower = chunk.lower()
    
    # If the chunk is very small, it's likely not useful
    if len(chunk) < 50:
        return False

    for tag in tags:
        # Basic keyword match. 
        # You can expand this with a dictionary of synonyms later.
        if tag.lower() in chunk_lower:
            return True
            
    return False