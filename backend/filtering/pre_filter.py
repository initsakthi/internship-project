import re

def is_relevant(chunk: str, tags: list) -> bool:
    """
    Surgically checks if a text chunk is worth the cost of an LLM call.
    Uses regex word boundaries and context clues for high accuracy.
    """
    # 1. Minimum Threshold: Avoid processing fragments or noise
    if not chunk or len(chunk) < 50:
        return False

    chunk_lower = chunk.lower()
    
    # 2. Define Context Clues / Synonyms
    # If a user provides a tag like 'Total', we should also look for 'Amount', etc.
    synonym_map = {
        "total": ["amount", "balance", "total", "sum", "$"],
        "date": ["date", "issued", "on:", "dated"],
        "invoice": ["invoice", "inv", "bill", "receipt"],
        "name": ["name", "customer", "client", "attention", "attn"],
        "address": ["address", "street", "city", "location", "zip"]
    }

    # 3. Build a Search Set
    # We combine the user's tags with our known synonyms
    search_terms = set()
    for tag in tags:
        tag_lower = tag.lower()
        search_terms.add(tag_lower)
        # Add synonyms if the tag matches one of our keys
        if tag_lower in synonym_map:
            search_terms.update(synonym_map[tag_lower])

    # 4. Perform Fast Regex Matching
    # Using \b (word boundaries) prevents 'date' from matching 'validate'
    pattern = r"\b(" + "|".join(re.escape(term) for term in search_terms) + r")\b"
    
    # Special case: $ and : don't always need word boundaries
    if any(re.search(pattern, chunk_lower) for pattern in [pattern, r"[\$:]"]):
        return True

    return False