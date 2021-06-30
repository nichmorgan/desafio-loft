from typing import AnyStr, Callable, List, Optional, Union
from datetime import datetime
from workalendar.america import BrazilSaoPauloState
import re

CALENDAR = BrazilSaoPauloState()


def __extract_by_regex(pattern: AnyStr, text: AnyStr, *,
                       flag: re.RegexFlag = re.MULTILINE,
                       group_index: Optional[int] = None, result_index: Optional[int] = 0,
                       parser: Callable = None, validator: Callable = None) -> Optional[Union[str, List[str]]]:
    """Base regex extractor.

    Args:
        pattern (AnyStr): Regex pattern.
        text (AnyStr): Target text.
        group_index (Optional[int]): Return result group by index
        result_index (Optional[int]): Return result value by index - 0 default.
        parser (Callable): Parses string value.
        validator (Callable): Validate value after parser.

    Returns:
        Optional[Union[str, List[str]]]: Regex result.
    """

    result_list = re.findall(pattern, text, flag)
    if group_index is not None:
        result_list = result_list[group_index]

    if len(result_list) > 0:
        if result_index is not None:
            result = result_list[result_index]
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

    return __extract_by_regex(r"(\d+)(?=.*\n1\.)", text, flag=re.DOTALL,
                              parser=int, validator=validator,
                              result_index=-1)


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

    return __extract_by_regex(r"(?<=3\.1\.).*?(((\d){1,3})+([.][\d]{3})*([,](\d)*)?)", text,
                              group_index=0, result_index=0,
                              parser=parser, validator=validator)


def extract_contract_date(text: AnyStr) -> Optional[datetime]:
    """Extract Contract date from text.

    Args:
        text (AnyStr): Text target.

    Returns:
        Optional[datetime]: Contract date or None
    """

    def parser(contract_date: str) -> datetime:
        return datetime.strptime(contract_date.replace("\n", ""), r"%d/%m/%Y")

    return __extract_by_regex(r"(?<=6\.2\.).*(\d{2}/\d{2}/\d{4})", text, flag=re.DOTALL,
                              parser=parser)


def extract_deed_date(text: AnyStr, contract_date: datetime) -> Optional[datetime]:
    """Extract deed date from text.

    Args:
        text (AnyStr): Text target.
        contract_date (datetime): Contract date.

    Returns:
        Optional[datetime]: Deed date or None
    """

    if not contract_date:
        raise ValueError("Contract date is None!")

    def parser(deed_days: str) -> datetime:
        return CALENDAR.add_working_days(contract_date, int(deed_days), keep_datetime=True)

    def validator(deed_date: datetime) -> Optional[datetime]:
        return deed_date if deed_date > contract_date else None

    return __extract_by_regex(r"(?<=5\.1\.).*?(\d+)", text, flag=re.DOTALL,
                              parser=parser, validator=validator)
