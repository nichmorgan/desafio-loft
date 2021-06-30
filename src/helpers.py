from datetime import datetime
from extractors import CALENDAR
from typing import Union
from pathlib import Path
import fitz


def extract_all_pages_text(file_path: Union[Path, str]) -> str:
    """Pdf pages text extrator.

    Args:
        file_path (Union[Path, str]): Pdf file path.

    Raises:
        FileExistsError: The file path is invalid!

    Returns:
        str: The pdf pages content appended by break lines.
    """

    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not (file_path.exists() or file_path.is_file()):
        raise FileExistsError(
            f"The file {file_path.absolute().as_posix()} not exists!")

    document = fitz.Document(file_path.absolute().as_posix())
    text: str = ""
    for page in document:
        text += "\n" + page.get_text()
    return text.strip()
