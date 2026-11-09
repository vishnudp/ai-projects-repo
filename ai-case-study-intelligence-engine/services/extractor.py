from pypdf import PdfReader
from docx import Document


def extract_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def extract_docx(file_path):

    doc = Document(file_path)

    return "\n".join(
        para.text for para in doc.paragraphs
    )


def extract_text(file_path):

    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    if file_path.endswith(".docx"):
        return extract_docx(file_path)

    return open(
        file_path,
        encoding="utf-8"
    ).read()