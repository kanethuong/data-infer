from .base_analysis import BaseAnalysis
import pandas as pd
import numpy as np
from api.utils import replace_null_values


class DatetimeAnalysis(BaseAnalysis):
    converted = None

    def __init__(self, series, threshold=0.8):
        super().__init__(series, threshold)
        self.series = replace_null_values(series)

    def is_applicable(self) -> bool:
        dtype_char = np.dtype(self.series.dtype).char
        test_size = 10
        max_test_size = len(self.series)

        if max_test_size == 0:
            return False

        current_head = self.series.head(test_size)

        while test_size < max_test_size and current_head.isna().all().all():
            test_size *= 2
            current_head = self.series.head(test_size)

        # Check if the current_head can be converted to datetime
        if self.can_convert_to_datetime(current_head):
            test_convert_rate = (
                1 - pd.to_datetime(current_head, errors="coerce").isna().mean()
            )
            is_threshold_met = test_convert_rate >= min(0.5, self.threshold)
            is_datetime_or_object = (
                dtype_char in np.typecodes["Datetime"] or dtype_char == "O"
            )

            return is_threshold_met and is_datetime_or_object
        else:
            return False

    def analyze(self):
        if self.series.dtype == "datetime64":
            return 1.0

        series_converted = pd.to_datetime(
            self.series, errors="coerce", dayfirst=True, format="mixed"
        )
        datetime_ratio = series_converted.notna().mean()
        self.converted = series_converted
        return datetime_ratio

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.analyze()
        return self.converted if self.converted is not None else self.series

    @staticmethod
    def can_convert_to_datetime(series):
        try:
            pd.to_datetime(series, errors="raise")
            return True
        except (ValueError, TypeError):
            return False
