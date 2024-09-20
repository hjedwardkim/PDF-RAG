from io import BytesIO

from PyPDF2 import PdfReader


def parse_pdf(content: bytes) -> list[str]:
    pdf = PdfReader(BytesIO(content))
    chunks = []
    for page in pdf.pages:
        text = page.extract_text()
        chunks.extend(text.split("\n\n"))

    return chunks
