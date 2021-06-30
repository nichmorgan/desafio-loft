from datetime import datetime
from typing import Any, AnyStr, Callable, List, Tuple, Union

import extractors
import helpers

from tests import helpers_test


def execute_extration(extract_function: Callable, text: str, pdf_path: str, **kwargs) -> Union[str, None]:
    pdf_file = helpers_test.generate_pdf(text, pdf_path)
    pdf_text = helpers.extract_all_pages_text(pdf_file)
    return extract_function(text=pdf_text, **kwargs)


def test_extract_unit_id(new_pdf_file_path: str, get_document_sample: Tuple[AnyStr, List[Any]]):
    text, result_expected = get_document_sample
    assert execute_extration(extractors.extract_unit_id,
                             text, new_pdf_file_path) == result_expected[0]


def test_extract_sale_price(new_pdf_file_path: str, get_document_sample: Tuple[AnyStr, List[Any]]):
    text, result_expected = get_document_sample
    assert execute_extration(extractors.extract_sale_price,
                             text, new_pdf_file_path) == result_expected[1]


def test_extract_contract_date(new_pdf_file_path: str, get_document_sample: Tuple[AnyStr, List[Any]]):
    text, result_expected = get_document_sample
    assert execute_extration(extractors.extract_contract_date,
                             text, new_pdf_file_path) == result_expected[2]


def test_extract_deed_date(get_document_sample: Tuple[AnyStr, List[Any]], new_pdf_file_path: str):
    text, result_expected = get_document_sample
    assert execute_extration(extractors.extract_deed_date,
                             text, new_pdf_file_path, contract_date=result_expected[2]) == result_expected[3]
