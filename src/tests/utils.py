from pathlib import Path
from typing import AnyStr, List, Union
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime


def generate_file_path(folder_path: Path, extension: AnyStr = "pdf") -> Path:
    return folder_path / f"tmp_file.{datetime.now().strftime(r'%Y%m%dT%H%M%S')}.{extension}"


def generate_pdf(text: str, pdf_path: Union[str, Path]) -> Path:
    pdf_path = pdf_path if isinstance(
        pdf_path, str) else pdf_path.absolute().as_posix()
    canvas = Canvas(pdf_path)
    for index, line in enumerate(text.splitlines()):
        canvas.drawString(72, 72 + 1 * index, line)
    canvas.save()
    return Path(pdf_path)


def generate_pdf_files(sample_list: List[str], folder_path: Path) -> None:
    for sample in sample_list:
        generate_pdf(sample, generate_file_path(folder_path))
