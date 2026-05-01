from pydantic import ValidationError
# Assuming your model is in models.py at the project root
from database.models import ExtractionRequest

def validate_extraction(data: dict):
    """
    Verifies the AI output. 
    You can also add logic here to calculate a 'Confidence Score'.
    """
    if not data:
        return None, 0.0

    # Example: Check how many keys are NOT null to determine confidence
    total_tags = len(data.keys())
    found_tags = len([v for v in data.values() if v is not None])
    
    confidence_score = (found_tags / total_tags) if total_tags > 0 else 0.0
    
    # Optional: You can use your Pydantic models to strictly validate types
    # try:
    #     # If you have a specific 'ExtractionResult' model, use it here
    #     return data, confidence_score
    # except ValidationError:
    #     return None, 0.0
    
    return data, confidence_score