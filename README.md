# 🛡️ PII Detection System

A full-stack application for detecting and extracting Personally Identifiable Information (PII) from structured and unstructured data using modern NLP techniques and a local LLM.

---

## 🚀 Overview

This project enables users to upload documents (PDF/images), process them through an intelligent pipeline, and extract sensitive information such as names, emails, phone numbers, and more.

It combines:

* Rule-based + NLP-based detection
* OCR for image handling
* Local LLM orchestration for intelligent extraction

---

## 🧱 Tech Stack

### 🔹 Backend

* FastAPI (Python)
* spaCy (NLP)
* pdfplumber (PDF processing)
* pytesseract (OCR for images)
* Ollama (Local LLM - Gemma)

### 🔹 Frontend

* Angular

### 🔹 Databases & Services

* MongoDB (data storage)
* Elasticsearch (search & indexing)
* XAMPP (optional local setup)

---

## ✨ Features

* 📄 Upload and process PDFs and images
* 🔍 Detect PII fields (name, email, phone, etc.)
* 🧠 LLM-powered intelligent extraction
* 🖼️ OCR support for image-based documents
* ⚡ Real-time API integration with frontend
* 📊 Structured JSON output

---

## 📸 Screenshots

### Upload Interface

![Upload Page](docs/screenshot/upload.png)

### Extraction Results

![Results](docs/screenshot/result.png)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pii-detection-system.git
cd pii-detection-system
```

---

## 🖥️ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

### ▶️ Run Backend

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

---

## 🌐 Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run Angular app
ng serve
```

Open in browser:

```
http://localhost:4200
```

---

## 🧠 LLM Setup (Ollama)

Install and run Ollama:

```bash
ollama serve
```

Pull the required model:

```bash
ollama pull gemma
```

---

## 🗄️ Required Services

Make sure these are running:

* MongoDB
* Elasticsearch
* Ollama (Local LLM)

---

## 📂 Project Structure

```bash
PII-Detection-System/
│── backend/
│── frontend/
│── docs/
│   └── screenshots/
│── README.md
│── .gitignore
```

---

## 📦 API Endpoints

| Endpoint                | Method | Description           |
| ----------------------- | ------ | --------------------- |
| `/extract`              | POST   | Structured extraction |
| `/extract-unstructured` | POST   | LLM-based extraction  |

---

## ⚠️ Notes

* Ensure Ollama is running before triggering extraction
* Supports PDF and image inputs (PNG, JPG)
* Large files may take longer due to OCR + LLM processing

---

## 🔮 Future Improvements

* Multi-language PII detection
* Region-specific identifiers (SSN, Aadhaar, PAN)
* Role-based access control
* Cloud deployment support
* Model optimization & caching

---

## 👨‍💻 Author

**Sakthivel Chandramohan**
MCA Student | Full Stack Developer | AI Enthusiast

---

## 📄 License

This project is for educational and research purposes.
