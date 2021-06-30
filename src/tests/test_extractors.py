from datetime import datetime, timedelta
from typing import Callable, Union
import pytest
from src import extractors, utils
import utils as test_utils


def execute_extration(extract_function: Callable, text: str, pdf_path: str, **kwargs) -> Union[str, None]:
    pdf_file = test_utils.generate_pdf(text, pdf_path)
    pdf_text = utils.extract_all_pages_text(pdf_file)
    return extract_function(text=pdf_text, **kwargs)


__UNIT_ID_TEXT = """COMPROMISSO DE COMPRA E VENDA
EDIFÍCIO LOFT
Rua Tabapuã, nº 745, Itaim.
942739
SP - SÃO PAULO
1."""
__UNIT_ID_TEXT_EXPECTED = 942739


@pytest.mark.parametrize("text", [__UNIT_ID_TEXT])
def test_extract_unit_id(text: str, new_pdf_file_path: str):
    assert execute_extration(extractors.extract_unit_id,
                             text, new_pdf_file_path) == __UNIT_ID_TEXT_EXPECTED


__SALE_PRICE_TEXT = """3. Do Valor da Compra e Venda
3.1. R$ 590.000,00 ( oitocentos mil reais)
4. Da Forma de Pagamento do Valor da Compra e Venda"""
__SALE_PRICE_TEXT_EXPECTED = 590e3


@pytest.mark.parametrize("text", [__SALE_PRICE_TEXT])
def test_extract_sale_price(text: str, new_pdf_file_path: str, **kwargs):
    kwargs.update(dict(text=text))
    assert execute_extration(extractors.extract_sale_price,
                             text, new_pdf_file_path) == __SALE_PRICE_TEXT_EXPECTED


__CONTRACT_DATE_TEXT = """6.2. O VENDEDOR observará os prazos previstos abaixo:
a) Apresentação da documentação solicitada pelo COMPRADOR: em até 5 (cinco) dias úteis
após a solicitação;
b) Apresentação de esclarecimentos adicionais (se aplicável): em até 5 (cinco) dias úteis após a
solicitação.
São Paulo, 13/04/2021"""
__CONTRACT_DATE_TEXT_EXPECTED = datetime(2021, 4, 13).date()


@pytest.mark.parametrize("text", [__CONTRACT_DATE_TEXT])
def test_extract_contract_date(text: str, new_pdf_file_path: str):
    assert execute_extration(extractors.extract_contract_date,
                             text, new_pdf_file_path) == __CONTRACT_DATE_TEXT_EXPECTED


__DEED_DATE_TEXT = """5. Da Escritura de Compra e Venda
5.1.
A Escritura deverá ser lavrada em até 100 (cem) dias corridos contados da assinatura do 
Compromisso, desde que o VENDEDOR apresente todos os documentos e/ou esclarecimentos 
solicitados pelo COMPRADOR e não haja pendências a serem regularizadas.
5.2.
Nesta mesma data, o VENDEDOR firmou Instrumento Particular de Compromisso de Compra e 
Venda com o INTERVENIENTE ANUENTE para aquisição, pelo VENDEDOR, do imóvel, localizado 
na SP - SÃO PAULO, na Rua Tabapuã, nº 745, Itaim."""
__DEED_DATE_TEXT_EXPECTED = datetime.now().date() + timedelta(days=100)


@pytest.mark.parametrize("text", [__DEED_DATE_TEXT])
@pytest.mark.parametrize("contract_date", [datetime.now().date()])
def test_extract_deed_date(text: str, contract_date: datetime.date, new_pdf_file_path: str):
    assert execute_extration(extractors.extract_deed_date,
                             text, new_pdf_file_path, contract_date=contract_date) == __DEED_DATE_TEXT_EXPECTED
