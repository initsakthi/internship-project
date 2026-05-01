import re
import spacy


try:
    nlp = spacy.load("en_core_web_lg")
except Exception as e:
    raise Exception("Please install en_core_web_trf first: python -m spacy download en_core_web_trf") from e



EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_REGEX = r'(\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{3,4}[-.\s]?\d{4})'
URL_REGEX = r'https?://[^\s]+'
DATE_REGEX = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b'



SECTION_HEADERS = {
    "summary": ["summary","objective","career objective","profile","about me"],
    "skills": ["skills","technical skills","skill set","technologies","expertise"],
    "education": ["education","academic","qualification","academics"],
    "experience": ["experience","work experience","professional experience","internship","employment"],
    "projects": ["projects","project work","academic projects","personal projects"],
    "certifications": ["certifications","certificates","certification"]
}



def extract_emails(text: str) -> list:
    return list(set(re.findall(EMAIL_REGEX, text)))

def extract_phones(text: str) -> list:
    matches = re.findall(PHONE_REGEX, text)
    valid = [m for m in matches if len(re.sub(r'\D', '', m)) >= 10]
    return list(set(valid))

def extract_urls(text: str) -> list:
    return list(set(re.findall(URL_REGEX, text)))

def extract_dates(text: str) -> list:
    return list(set(re.findall(DATE_REGEX, text)))



def extract_entities(text: str) -> dict:
    """
    Extracts all entities using SpaCy transformer model
    Returns a dictionary where key = entity label, value = list of entity strings
    """
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        entities[ent.label_].append(ent.text)
    
    
    for label in entities:
        entities[label] = list(set(entities[label]))
    
    return entities



def extract_sections(text: str) -> dict:
    found_sections = {}
    lower_text = text.lower()
    for section, keywords in SECTION_HEADERS.items():
        for kw in keywords:
            if kw in lower_text:
                found_sections[section] = True
    return found_sections
