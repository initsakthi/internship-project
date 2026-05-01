import re

def normalize(text: str) -> str:
    """Cleans text by removing extra whitespace and non-printable characters."""
    if not text:
        return ""
    
    # Remove non-printable characters
    text = "".join(char for char in text if char.isprintable())
    
    # Replace multiple newlines/spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()