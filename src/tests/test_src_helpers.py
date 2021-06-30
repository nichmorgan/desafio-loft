import pytest
from tests import helpers_test
import helpers


@pytest.mark.parametrize("text", ["Test String!", "Test value!", "It's okay!"])
def test_extract_all_pages_text(text: str, new_pdf_file_path: str):
    pdf_path = helpers_test.generate_pdf(text, new_pdf_file_path)
    assert helpers.extract_all_pages_text(pdf_path) == text
