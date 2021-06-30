from typing import Union
from pathlib import Path
import PyPDF2


def extract_all_pages_text(file_path: Union[Path, str]) -> str:
    """Pdf pages text extrator.

    Args:
        file_path (Union[Path, str]): Pdf file path.

    Raises:
        FileExistsError: The file path is invalid!

    Returns:
        str: The pdf pages content appended by break lines.
    """

    if not (file_path.exists() or file_path.is_file()):
        raise FileExistsError(
            f"The file {file_path.absolute().as_posix()} not exists!")
    with open(file_path, "rb") as file:
        file_reader = PyPDF2.PdfFileReader(file)
        text: str = ""
        for page in file_reader.pages:
            text += "\n" + page.extractText()
        return text.strip()
