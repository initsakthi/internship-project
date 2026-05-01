def split_by_tokens(text: str, chunk_size: int = 2000, overlap: int = 200):
    """Splits text into chunks. 1 token is roughly 4 characters."""
    # Using character-to-token approximation (4 chars ~= 1 token)
    char_chunk_size = chunk_size * 4
    char_overlap = overlap * 4
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + char_chunk_size
        chunks.append(text[start:end])
        start += (char_chunk_size - char_overlap)
        
    return chunks