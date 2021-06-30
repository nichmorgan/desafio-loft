from typing import Any, AnyStr, List, Tuple
import file_processor


def test_text_processor(get_document_sample: Tuple[AnyStr, List[Any]]):
    text, data = get_document_sample
    dataframe_test = file_processor.process_text_to_series(text)
    data[2] = data[2].strftime(r"%d/%m/%Y")
    data[3] = data[3].strftime(r"%d/%m/%Y")
    assert dataframe_test.values.tolist() == data
