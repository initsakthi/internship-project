import os
import pdfplumber
import docx
import pytesseract
import cv2
import numpy as np
from pdf2image import convert_from_path

# =========================
# WINDOWS PATH CONFIG
# =========================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"

# =========================
# IMAGE PREPROCESS
# =========================

def preprocess_image(image):
    open_cv_image = np.array(image)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    height, width = gray.shape

    if width < 2000:
        scale = 2000 / width
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    gray = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

    if gray.max() - gray.min() < 100:
        gray = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            2
        )

    return gray


# =========================
# PDF DIGITAL + OCR (PAGE AWARE)
# =========================

def extract_from_pdf(file_path: str):
    pages_output = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()

                if page_text and page_text.strip():
                    pages_output.append({
                        "page": page_number,
                        "text": page_text
                    })

        if pages_output:
            print("Digital PDF detected.")
            return pages_output

        print("Scanned PDF detected. Switching to OCR...")

        return extract_pdf_with_ocr(file_path)

    except Exception as e:
        print(f"PDF error: {e}")
        return []


def extract_pdf_with_ocr(file_path: str):
    pages_output = []

    try:
        pages = convert_from_path(
            file_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )

        for page_number, page in enumerate(pages, start=1):
            processed = preprocess_image(page)

            page_text = pytesseract.image_to_string(
                processed,
                config="--oem 3 --psm 6"
            )

            pages_output.append({
                "page": page_number,
                "text": page_text
            })

    except Exception as e:
        print(f"OCR error: {e}")

    return pages_output


# =========================
# DOCX (TREATED AS PAGE 1)
# =========================

def extract_from_docx(file_path: str):
    try:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return [{"page": 1, "text": text}]
    except Exception as e:
        print(f"DOCX error: {e}")
        return []


# =========================
# MAIN ENTRY
# =========================

def extract_text(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_from_pdf(file_path)

    elif ext in [".docx", ".doc"]:
        return extract_from_docx(file_path)

    elif ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return [{"page": 1, "text": f.read()}]
        except:
            return []

    return []
