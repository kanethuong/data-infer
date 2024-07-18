import pandas as pd
from .exceptions import UnsupportedFileFormatError


def read_file(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path, low_memory=False)
    elif file_path.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file_path, engine="openpyxl")
    else:
        raise UnsupportedFileFormatError(
            "Unsupported file format. Please use CSV or Excel files."
        )
    return df
