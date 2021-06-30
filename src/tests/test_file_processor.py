from pathlib import Path
from typing import Tuple
import utils as test_utils
from src.file_processor import process_files_to_dataframe


def test_file_processor(tmp_path: Path, full_document_sample):
    text, data = full_document_sample

    test_utils.generate_pdf_files([text], tmp_path)
    dataframe = process_files_to_dataframe(tmp_path, "*.pdf")
    assert len(dataframe) == 1
