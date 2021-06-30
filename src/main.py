from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from pandas import DataFrame

from file_processor import process_files_to_dataframe


if __name__ == "__main__":
    load_dotenv()

    base_extraction_folder = getenv("BASE_TARGET_FOLDER")
    target_file_pattern = getenv("TARGET_FILE_PATTERN")
    extraction_output_path = getenv("EXTRACTION_OUTPUT_FOLDER")

    if not base_extraction_folder:
        raise ValueError("Base extraction folder not found!")
    if not target_file_pattern:
        raise ValueError("Target file pattern not found!")
    if not extraction_output_path:
        raise ValueError("Extraction output path not found!")

    extraction_output_path = Path(extraction_output_path)
    extraction_output_path.mkdir(parents=True, exist_ok=True)

    dataframe: DataFrame = process_files_to_dataframe(base_extraction_folder,
                                                      target_file_pattern)
    output_file = extraction_output_path / "output.xlsx"
    dataframe.to_excel(output_file.absolute().as_posix(), index=False)
