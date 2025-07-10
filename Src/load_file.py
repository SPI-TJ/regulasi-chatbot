# file: load_file.py
import pandas as pd
import pytesseract
import docx
import os
import io
import logging
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader

# Setup logging
logging.basicConfig(level=logging.INFO)

def load_pdf(file):
    try:
        file_bytes = file.read()
        logging.info("🔍 Membaca file PDF...")

        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

        if text.strip():
            logging.info("✅ Teks berhasil diekstrak dari PDF.")
            return text

        logging.warning("⚠️ PDF tidak mengandung teks, menjalankan OCR...")
        images = convert_from_bytes(file_bytes)
        ocr_text = ""
        for i, image in enumerate(images):
            ocr_text += f"\n--- Page {i+1} ---\n"
            ocr_text += pytesseract.image_to_string(image)

        return "📷 [OCR digunakan karena PDF tidak mengandung teks.]\n" + ocr_text.strip()

    except Exception as e:
        logging.error(f"❌ Gagal memproses PDF: {e}")
        return f"❌ Gagal memproses PDF: {e}"

def load_docx(file):
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        logging.info("✅ Dokumen DOCX berhasil dibaca.")
        return text
    except Exception as e:
        logging.error(f"❌ Gagal memproses DOCX: {e}")
        return f"❌ Gagal memproses DOCX: {e}"

def load_excel(file):
    try:
        df = pd.read_excel(file)
        logging.info(f"✅ File Excel berhasil dibaca dengan shape: {df.shape}")
        return df.to_markdown(index=False)
    except Exception as e:
        logging.error(f"❌ Gagal memproses Excel: {e}")
        return f"❌ Gagal memproses Excel: {e}"

def load_csv(file):
    try:
        df = pd.read_csv(file)
        logging.info(f"✅ File CSV berhasil dibaca dengan shape: {df.shape}")
        return df.to_markdown(index=False)
    except Exception as e:
        logging.error(f"❌ Gagal memproses CSV: {e}")
        return f"❌ Gagal memproses CSV: {e}"

def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name
    file_ext = os.path.splitext(filename)[1].lower()
    logging.info(f"📂 File diterima: {filename} (ekstensi: {file_ext})")

    if file_ext == ".pdf":
        return load_pdf(uploaded_file)
    elif file_ext in [".docx"]:
        return load_docx(uploaded_file)
    elif file_ext in [".xlsx", ".xls"]:
        return load_excel(uploaded_file)
    elif file_ext == ".csv":
        return load_csv(uploaded_file)
    else:
        logging.warning(f"❌ Format file tidak didukung: {file_ext}")
        return "❌ Format file tidak didukung. Silakan upload PDF, DOCX, Excel, atau CSV."