import pdfplumber

def get_pages(file_path: str):
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            print(f" Page {i} text length: {len(text) if text else 0}") # Add this!
            if text:
                yield text