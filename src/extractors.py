import enum
from sys import flags
from typing import AnyStr, Callable, List, Optional, Union
from datetime import date, timedelta, datetime
import re


def __extract_by_regex(pattern: AnyStr, text: AnyStr, *,
                       flag: re.RegexFlag = re.MULTILINE, only_first=True,
                       parser: Callable = None, validator: Callable = None) -> Optional[Union[str, List[str]]]:
    """Base regex extractor.

    Args:
        pattern (AnyStr): Regex pattern.
        text (AnyStr): Target text.
        only_first (bool): Return only the first result.
        parser (Callable): Parses string value.
        validator (Callable): Validate value after parser.

    Returns:
        Optional[Union[str, List[str]]]: Regex result.
    """

    result_list = re.findall(pattern, text, flag)
    if len(result_list) > 0:
        if only_first:
            result = result_list[0]
            if parser:
                result = parser(result)
            if validator:
                result = validator(result)
            return result

        if parser or validator:
            for index in range(len(result_list)):
                if parser:
                    result_list[index] = parser(result_list[index])
                if validator:
                    result_list[index] = validator(result_list[index])
        return result_list

    return None


def extract_unit_id(text: AnyStr) -> Optional[int]:
    """Extract Unit id from text.

    Args:
        text (AnyStr): Text target.

    Returns:
        Optional[str]: Unit id or None
    """

    def validator(unit_id: int) -> Optional[int]:
        return unit_id if unit_id > 0 else None

    return __extract_by_regex(r"(\d+)(?=\n.*1\.)", text, parser=int, validator=validator, flag=re.DOTALL)


def extract_sale_price(text: AnyStr) -> Optional[float]:
    """Extract Sale price from text.

    Args:
        text (AnyStr): Text target.

    Returns:
        Optional[float]: Sale price or None
    """

    def parser(price: str) -> float:
        return float(price.replace(".", "").replace(",", "."))

    def validator(price: float) -> Optional[float]:
        return price if price > 0 else None

    return __extract_by_regex(r"(?<=3\.1\.).*?(\d*\.?\d*,\d{2})(?=\s\()", text, parser=parser, validator=validator)


def extract_contract_date(text: AnyStr) -> Optional[datetime.date]:
    """Extract Contract date from text.

    Args:
        text (AnyStr): Text target.

    Returns:
        Optional[datetime.date]: Contract date or None
    """

    def parser(contract_date: str) -> datetime.date:
        return datetime.strptime(contract_date, r"%d/%m/%Y").date()

    return __extract_by_regex(r"(?<=6\.2\.).*(\d{2}/\d{2}/\d{4})", text, flag=re.DOTALL, parser=parser)


def extract_deed_date(text: AnyStr, contract_date: datetime.date) -> Optional[datetime.date]:
    """Extract deed date from text.

    Args:
        text (AnyStr): Text target.

    Returns:
        Optional[datetime.date]: Deed date or None
    """

    def parser(deed_days: str) -> datetime.date:
        return contract_date + timedelta(days=int(deed_days))

    def validator(deed_date: datetime.date) -> Optional[datetime.date]:
        return deed_date if deed_date > contract_date else None

    return __extract_by_regex(r"(?<=5\.1\.).*?(\d+)", text, flag=re.DOTALL, parser=parser, validator=validator)
