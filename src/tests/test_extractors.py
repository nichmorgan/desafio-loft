from datetime import datetime
from typing import AnyStr, Callable, Tuple, Union

from src import extractors, utils

import utils as test_utils


def execute_extration(extract_function: Callable, text: str, pdf_path: str, **kwargs) -> Union[str, None]:
    pdf_file = test_utils.generate_pdf(text, pdf_path)
    pdf_text = utils.extract_all_pages_text(pdf_file)
    return extract_function(text=pdf_text, **kwargs)


def test_extract_unit_id(new_pdf_file_path: str, unit_id_sample: Tuple[AnyStr, int]):
    text, result_expected = unit_id_sample
    assert execute_extration(extractors.extract_unit_id,
                             text, new_pdf_file_path) == result_expected


def test_extract_sale_price(new_pdf_file_path: str, sale_price_sample: Tuple[AnyStr, float]):
    text, result_expected = sale_price_sample
    assert execute_extration(extractors.extract_sale_price,
                             text, new_pdf_file_path) == result_expected


def test_extract_contract_date(new_pdf_file_path: str, contract_date_sample: Tuple[AnyStr, datetime.date]):
    text, result_expected = contract_date_sample
    assert execute_extration(extractors.extract_contract_date,
                             text, new_pdf_file_path) == result_expected


def test_extract_deed_date(deed_date_sample: Tuple[AnyStr, datetime.date, datetime.date], new_pdf_file_path: str):
    text, contract_date, result_expected = deed_date_sample
    assert execute_extration(extractors.extract_deed_date,
                             text, new_pdf_file_path, contract_date=contract_date) == result_expected
