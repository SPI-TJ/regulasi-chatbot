import pandas as pd
import pytesseract
import docx
import os
import io
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader

def load_pdf(file):
    try:
        # Simpan file ke bytes
        file_bytes = file.read()

        # Baca pakai PdfReader dulu (try plain text)
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

        if text.strip():
            return text
        
        # Fallback ke OCR kalau teks kosong
        images = convert_from_bytes(file_bytes)
        ocr_text = ""
        for i, image in enumerate(images):
            ocr_text += f"\n--- Page {i+1} ---\n"
            ocr_text += pytesseract.image_to_string(image)

        return "📷 [OCR digunakan karena PDF tidak mengandung teks.]\n" + ocr_text.strip()

    except Exception as e:
        return f"❌ Gagal memproses PDF: {e}"

def load_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def load_excel(file):
    df = pd.read_excel(file)    
    return df.to_string()

def load_csv(file):
    df = pd.read_csv(file)
    return df.to_string()

def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext == ".pdf":
        return load_pdf(uploaded_file)
    elif file_ext in [".docx"]:
        return load_docx(uploaded_file)
    elif file_ext in [".xlsx", ".xls"]:
        return load_excel(uploaded_file)
    elif file_ext == ".csv":
        return load_csv(uploaded_file)
    else:
        return "❌ Format file tidak didukung. Silakan upload PDF, DOCX, Excel, atau CSV."
