import numpy as np
import pandas as pd


def replace_null_values(value: pd.Series) -> pd.Series:
    # List of string values to be considered as null
    strs_null_values = {
        "not available",
        "n/a",
        "na",
        "nan",
        "none",
        "null",
        "missing",
        "not found",
    }

    # Convert the Series to lower case and check if values are in the set of null values
    nulls_index = value.apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
        strs_null_values | {np.nan}
    )

    # Replace identified nulls with np.nan
    return value.where(~nulls_index, np.nan)
