from layout_parser import parse_layout_from_pdf
from load_file import extract_text_from_file

def extract_all(file):
    filename = file.name
    file_ext = filename.split(".")[-1].lower()

    file_bytes = file.read()
    file.seek(0)

    extracted_text = extract_text_from_file(file)

    layout_data = []
    if file_ext == "pdf":
        layout_data = parse_layout_from_pdf(file_bytes)

    return {
        "text": extracted_text,
        "layout": layout_data
    }
