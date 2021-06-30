from datetime import datetime
from typing import AnyStr, Tuple, Annotated
import pandas as pd
from pathlib import Path
from helpers import extract_all_pages_text
import extractors


__DEFAULT_HEADER = ("Unit_id", "Valor_Total",
                    "Data_Contrato", "Data_Excritura")
__HEADER_TYPE = Annotated[Tuple[AnyStr], len(__DEFAULT_HEADER)]
__OUTPUT_DATE_PATTERN = r"%d/%m/%Y"


def process_text_to_series(text: str, header: __HEADER_TYPE = __DEFAULT_HEADER) -> pd.DataFrame:
    unit_id: int = extractors.extract_unit_id(text)
    sale_price: float = extractors.extract_sale_price(text)
    contract_date: datetime = extractors.extract_contract_date(text)
    deed_date: datetime = extractors.extract_deed_date(text, contract_date)

    data = [unit_id, sale_price,
            contract_date, deed_date]
    if any([d is None for d in data]):
        raise ValueError("Any value not found!")

    data[2] = contract_date.strftime(__OUTPUT_DATE_PATTERN)
    data[3] = deed_date.strftime(__OUTPUT_DATE_PATTERN)

    return pd.Series(data, index=header)


def process_files_to_dataframe(base_folder: AnyStr, path_pattern: AnyStr, header: __HEADER_TYPE = __DEFAULT_HEADER) -> pd.DataFrame:
    dataframe = pd.DataFrame(columns=header)
    file_list = list(Path(base_folder).glob(path_pattern))
    for file in file_list:
        text = extract_all_pages_text(file)
        series = process_text_to_series(text, header)
        dataframe = dataframe.append(series, ignore_index=True)

    return dataframe
