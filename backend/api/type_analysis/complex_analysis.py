from .base_analysis import BaseAnalysis
import numpy as np
from api.utils import replace_null_values


class ComplexAnalysis(BaseAnalysis):
    converted = None

    def __init__(self, series, threshold=0.8):
        super().__init__(series, threshold)
        # Convert any null values in string to np.nan
        self.series = replace_null_values(series)

    def is_applicable(self) -> bool:
        sample_data = self.series.head()
        # Ensure that the sample data is not all null
        while sample_data.isna().all() and len(sample_data) < len(self.series):
            sample_data = self.series.head(len(sample_data) * 2)
        type_code = np.dtype(sample_data.dtype).char
        # Only applicable if the column is of complex type or object type
        return type_code in np.typecodes["Complex"] or type_code == "O"

    def analyze(self):
        series_converted = self.series.apply(self.convert_to_complex)
        complex_ratio = series_converted.notna().mean()
        self.converted = series_converted
        return complex_ratio

    @staticmethod
    def convert_to_complex(value):
        try:
            return complex(value)
        except (ValueError, TypeError):
            return np.nan

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.analyze()
        return self.converted if self.converted is not None else self.series
