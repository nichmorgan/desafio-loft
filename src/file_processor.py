from typing import AnyStr, Tuple, Annotated
import pandas as pd
from pathlib import Path
from src.utils import extract_all_pages_text
from src import extractors


__DEFAULT_HEADER = ("Unit Id", "Sale Price", "Contract Date", "Deed Date")
__HEADER_TYPE = Annotated[Tuple[AnyStr], len(__DEFAULT_HEADER)]


def process_files_to_dataframe(base_folder: AnyStr, path_pattern: AnyStr, header: __HEADER_TYPE = __DEFAULT_HEADER) -> pd.DataFrame:
    dataframe = pd.DataFrame(columns=header)
    file_list = list(Path(base_folder).glob(path_pattern))
    for file in file_list:
        text = extract_all_pages_text(file)
        unit_id = extractors.extract_unit_id(text)
        sale_price = extractors.extract_sale_price(text)
        contract_date = extractors.extract_contract_date(text)
        deed_date = extractors.extract_deed_date(text, contract_date)

        series = pd.Series([unit_id, sale_price,
                            contract_date, deed_date], index=header)
        dataframe = dataframe.append(series, ignore_index=True)

    return dataframe
