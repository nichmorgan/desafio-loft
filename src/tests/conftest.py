from datetime import datetime
from pathlib import Path
from typing import Tuple

import pytest
from dotenv import load_dotenv
from os import getenv
from extractors import CALENDAR
import helpers

from tests import helpers_test

load_dotenv()

################################################
#################  CONSTANTS ###################
################################################
__TEST_DATA_FOLDER = Path(getenv("BASE_TARGET_FOLDER")) / "test"

################################################
########## FILE SYSTEM FIXTURES ################
################################################


@pytest.fixture
def new_pdf_file_path(tmp_path: Path) -> str:
    return helpers_test.generate_file_path(tmp_path).absolute().as_posix()


################################################
######### SAMPLES FIXTURES #####################
################################################

@pytest.fixture
def get_document_sample() -> str:
    contract_date = datetime(2021, 4, 13)
    deed_date = CALENDAR.add_working_days(contract_date, 100,
                                          keep_datetime=True)
    data = [942739,  590.e3, contract_date, deed_date]
    file = list(__TEST_DATA_FOLDER.glob("*.pdf"))[0]
    return helpers.extract_all_pages_text(file.as_posix()), data
