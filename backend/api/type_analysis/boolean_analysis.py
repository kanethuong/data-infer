from .base_analysis import BaseAnalysis
from api.utils import replace_null_values
import numpy as np


class BooleanAnalysis(BaseAnalysis):
    TRUTHY_VALUES = ["true", "t", "yes", "y", "1"]
    FALSY_VALUES = ["false", "f", "no", "n", "0", "nan"]
    converted = None

    def __init__(self, series, threshold=0.8):
        super().__init__(series, threshold)
        # Convert any null values in string to np.nan
        self.series = replace_null_values(series)

    def is_applicable(self) -> bool:
        uniques = len(self.series.unique())
        allowed_uniques = len(self.TRUTHY_VALUES) + len(self.FALSY_VALUES) + 3 # 3 is the room for other additional posible values

        data_type = self.series.dtype
        dtype_char = np.dtype(data_type).char # get the character code of the data type

        is_valid_type = (
            data_type == "bool"
            or data_type == "object"
            or dtype_char in np.typecodes["AllInteger"] # in case boolean values are reprensented by 0 and 1
        )

        return uniques <= allowed_uniques and is_valid_type

    def analyze(self):
        bool_ratio = (
            self.series.dropna()
            .str.lower()
            .isin(self.TRUTHY_VALUES + self.FALSY_VALUES)
            .mean()
        )

        def convert_bool(x):
            if str(x).lower() in self.TRUTHY_VALUES:
                return True
            if str(x).lower() in self.FALSY_VALUES:
                return False
            return np.nan

        series_converted = self.series.apply(convert_bool)
        self.converted = series_converted
        return bool_ratio

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.analyze()
        return self.converted if self.converted is not None else self.series
