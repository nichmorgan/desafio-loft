from pathlib import Path
from datetime import datetime
import pytest


@pytest.fixture
def new_pdf_file_path(tmp_path: Path) -> str:
    pdf_file = tmp_path / \
        f"tmp_file.{datetime.now().strftime(r'%Y%m%dT%H%M%S')}.pdf"
    yield pdf_file.absolute().as_posix()
