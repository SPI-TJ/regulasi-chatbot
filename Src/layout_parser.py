import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import io
import re

def parse_layout_from_pdf(file_bytes):
    result = []
    images = convert_from_bytes(file_bytes)

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            halaman = i + 1
            page_text = page.extract_text()
            final_text = ""

            # OCR fallback jika extract_text gagal total
            if not page_text or not page_text.strip():
                page_text = pytesseract.image_to_string(images[i])

            # Clean whitespace dan baris kosong
            lines = page_text.splitlines()
            cleaned_lines = [line.strip() for line in lines if line.strip()]

            # Deteksi heading dan format
            formatted_lines = []
            for line in cleaned_lines:
                if re.match(r"^(?:[IVXLC]+|\d+)\.\s+.+", line):
                    formatted_lines.append(f"🟩 Heading: {line}")
                else:
                    formatted_lines.append(line)

            final_text = "\n".join(formatted_lines)

            # Deteksi tabel
            table_blocks = page.extract_tables()
            table_texts = []
            for t in table_blocks:
                table_text = "\n".join([" | ".join(str(cell or "") for cell in row) for row in t])
                table_texts.append(table_text)

            # Gabungkan semua isi (teks + tabel)
            gabungan = f"📄 Halaman {halaman}\n{'-'*30}\n{final_text}"
            for idx, tbl in enumerate(table_texts):
                gabungan += f"\n\n📊 Tabel {idx+1} (Hlm {halaman})\n{'-'*20}\n{tbl.strip()}"

            result.append({
                "halaman": halaman,
                "konten": gabungan
            })

    return result