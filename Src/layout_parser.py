# file: layout_parser.py

import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import io
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def extract_text_lines(page, image):
    try:
        text = page.extract_text()
        if not text or not text.strip():
            logging.warning("⚠️ Halaman kosong, fallback ke OCR.")
            text = pytesseract.image_to_string(image)
        lines = text.splitlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        logging.error(f"❌ Gagal mengekstrak teks dari halaman: {e}")
        return []

def format_lines(lines):
    formatted = []
    for line in lines:
        # Deteksi heading (misal: 1. ..., I. ..., A. ...)
        if re.match(r"^(?:[IVXLC]+|\d+|\w)\.\s+.+", line):
            formatted.append(f"🟩 Heading: {line}")
        else:
            formatted.append(line)
    return "\n".join(formatted)

def extract_tables(page):
    tables = page.extract_tables()
    table_texts = []
    for idx, table in enumerate(tables):
        try:
            table_str = "\n".join(
                [" | ".join(str(cell or "") for cell in row) for row in table]
            )
            table_texts.append(table_str.strip())
        except Exception as e:
            logging.error(f"❌ Error saat membaca tabel di halaman: {e}")
    return table_texts

def parse_layout_from_pdf(file_bytes):
    result = []
    try:
        images = convert_from_bytes(file_bytes)
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                logging.info(f"📄 Memproses halaman {i+1}...")
                image = images[i]

                lines = extract_text_lines(page, image)
                formatted_text = format_lines(lines)

                tables = extract_tables(page)
                page_content = f"📄 Halaman {i+1}\n{'-'*30}\n{formatted_text}"
                for t_idx, t in enumerate(tables):
                    page_content += f"\n\n📊 Tabel {t_idx+1} (Hlm {i+1})\n{'-'*20}\n{t}"

                result.append({
                    "halaman": i + 1,
                    "konten": page_content
                })

    except Exception as e:
        logging.error(f"❌ Gagal parsing layout PDF: {e}")
        result.append({
            "halaman": 0,
            "konten": f"❌ Gagal parsing layout PDF: {e}"
        })

    return result
