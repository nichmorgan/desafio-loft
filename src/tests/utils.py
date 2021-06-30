from pathlib import Path
from reportlab.pdfgen.canvas import Canvas


def generate_pdf(text: str, pdf_path: str) -> Path:
    canvas = Canvas(pdf_path)
    for index, line in enumerate(text.splitlines()):
        canvas.drawString(72, 72 + 1 * index, line)
    canvas.save()
    return Path(pdf_path)
