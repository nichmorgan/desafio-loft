from pathlib import Path
from datetime import datetime, timedelta
import utils as test_utils
from typing import Any, Dict, Tuple, Union
import pytest


################################################
########## FILE SYSTEM FIXTURES ################
################################################

@pytest.fixture
def new_pdf_file_path(tmp_path: Path) -> str:
    return test_utils.generate_file_path(tmp_path).absolute().as_posix()


################################################
######### SAMPLES FIXTURES #####################
################################################

@pytest.fixture
def unit_id_sample() -> Tuple[str, int]:
    text = """COMPROMISSO DE COMPRA E VENDA
    EDIFÍCIO LOFT
    Rua Tabapuã, nº 745, Itaim.
    942739
    SP - SÃO PAULO
    1."""
    result_expected = 942739

    return text, result_expected


@pytest.fixture
def sale_price_sample() -> Tuple[str, float]:
    text = """3. Do Valor da Compra e Venda
    3.1. R$ 590.000,00 ( oitocentos mil reais)
    4. Da Forma de Pagamento do Valor da Compra e Venda"""
    result_expected = 590.e3

    return text, result_expected


@pytest.fixture
def contract_date_sample() -> Tuple[str, datetime.date]:
    text = """6.2. O VENDEDOR observará os prazos previstos abaixo:
    a) Apresentação da documentação solicitada pelo COMPRADOR: em até 5 (cinco) dias úteis
    após a solicitação;
    b) Apresentação de esclarecimentos adicionais (se aplicável): em até 5 (cinco) dias úteis após a
    solicitação.
    São Paulo, 13/04/2021"""
    result_expected = datetime(2021, 4, 13).date()

    return text, result_expected


@pytest.fixture
def deed_date_sample() -> Tuple[str, datetime.date, datetime.date]:
    text = """5. Da Escritura de Compra e Venda
    5.1.
    A Escritura deverá ser lavrada em até 100 (cem) dias corridos contados da assinatura do 
    Compromisso, desde que o VENDEDOR apresente todos os documentos e/ou esclarecimentos 
    solicitados pelo COMPRADOR e não haja pendências a serem regularizadas.
    5.2.
    Nesta mesma data, o VENDEDOR firmou Instrumento Particular de Compromisso de Compra e 
    Venda com o INTERVENIENTE ANUENTE para aquisição, pelo VENDEDOR, do imóvel, localizado 
    na SP - SÃO PAULO, na Rua Tabapuã, nº 745, Itaim."""
    contract_date = datetime.now().date()
    result_expected = contract_date + timedelta(days=100)

    return text, contract_date, result_expected


@pytest.fixture
def full_document_sample(unit_id_sample, sale_price_sample, contract_date_sample, deed_date_sample) -> Tuple[str, Dict[str, Any]]:
    unit_id_text, unit_id = unit_id_sample
    sale_price_text, sale_price = sale_price_sample
    contract_date_text, contract_date = contract_date_sample

    deed_date_text, _, deed_date = deed_date_sample
    deed_time_delta = deed_date - datetime.now().date()
    deed_date = contract_date + deed_time_delta

    document = "\n".join([unit_id_text, sale_price_text,
                         contract_date_text, deed_date_text])
    data = dict(unit_id=unit_id, sale_price=sale_price,
                contract_date=contract_date, deed_date=deed_date)

    return document, data
