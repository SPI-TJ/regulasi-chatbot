# file: extractor.py

import logging
from Src.layout_parser import parse_layout_from_pdf
from Src.load_file import extract_text_from_file
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

def extract_all(file):
    filename = file.name
    file_ext = os.path.splitext(filename)[1].lower()

    logging.info(f"🚀 Mulai ekstraksi dokumen: {filename}")

    try:
        # Backup isi file untuk layout parsing
        file_bytes = file.read()
        file.seek(0)

        # Ekstrak teks secara general
        logging.info("📤 Mengekstrak isi teks dokumen...")
        extracted_text = extract_text_from_file(file)
        file.seek(0)

        layout_data = []
        if file_ext == ".pdf":
            logging.info("📐 Parsing layout PDF...")
            layout_data = parse_layout_from_pdf(file_bytes)

        # NOTE: Layout parsing DOCX/CSV/Excel belum didukung
        elif file_ext in [".docx", ".xlsx", ".xls", ".csv"]:
            logging.info("ℹ️ File bukan PDF, layout tidak diparsing.")

        return {
            "filename": filename,
            "file_ext": file_ext,
            "text": extracted_text,
            "layout": layout_data,
            "status": "success" if "❌" not in extracted_text else "error"
        }

    except Exception as e:
        logging.error(f"❌ Gagal mengekstrak dokumen: {e}")
        return {
            "filename": filename,
            "file_ext": file_ext,
            "text": f"❌ Gagal mengekstrak dokumen: {e}",
            "layout": [],
            "status": "error"
        }
