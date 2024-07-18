from .base_analysis import BaseAnalysis
import pandas as pd
import numpy as np
from api.utils import replace_null_values


class NumericAnalysis(BaseAnalysis):
    converted = None

    def __init__(self, series, threshold=0.8):
        super().__init__(series, threshold)
        self.series = replace_null_values(series)

    def is_applicable(self) -> bool:
        type_code = np.dtype(self.series.dtype).char
        return (
            type_code in np.typecodes["AllInteger"] + np.typecodes["AllFloat"]
            or type_code == "O"
        )

    def analyze(self):
        series_converted = pd.to_numeric(self.series, errors="coerce")
        numeric_ratio = series_converted.notna().mean()

        if series_converted.isna().all():
            return 0.0, 0.0, 0.0

        # Second conversion to float
        series_converted_float = pd.to_numeric(
            series_converted, errors="coerce", downcast="float"
        )
        float_ratio = series_converted_float.notna().mean()

        # Check if all values are integers or NaNs
        is_integer_or_na = series_converted_float.apply(
            lambda x: pd.isna(x) or float(x).is_integer()
        )

        if is_integer_or_na.all():
            # Downcast to appropriate integer type
            if series_converted_float.min() >= 0:
                series_converted_int = pd.to_numeric(
                    series_converted_float, errors="coerce", downcast="unsigned"
                )
            else:
                series_converted_int = pd.to_numeric(
                    series_converted_float, errors="coerce", downcast="integer"
                )
            int_ratio = series_converted_int.notna().mean()
        else:
            int_ratio = 0.0

        self.converted = (
            series_converted_float if int_ratio == 0.0 else series_converted_int
        )
        return numeric_ratio, int_ratio, float_ratio

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.analyze()
        return self.converted if self.converted is not None else self.series
