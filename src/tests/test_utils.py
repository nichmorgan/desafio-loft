import pytest
import utils as test_utils
from src import utils


@pytest.mark.parametrize("text", ["Test String!", "Test value!", "It's okay!"])
def test_extract_all_pages_text(text: str, new_pdf_file_path: str):
    pdf_path = test_utils.generate_pdf(text, new_pdf_file_path)
    assert utils.extract_all_pages_text(pdf_path) == text
