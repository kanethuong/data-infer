from .base_analysis import BaseAnalysis
import pandas as pd
from api.utils import replace_null_values


class CategoryAnalysis(BaseAnalysis):
    converted = None

    def __init__(self, series, threshold=0.8):
        super().__init__(series, threshold)
        self.series = replace_null_values(series)

    def is_applicable(self) -> bool:
        if self.series.nunique() > 50:
            return False
        # Check if the series contains datetime-like strings
        if self.series.dropna().apply(lambda x: self.is_datetime_string(x)).all():
            return False

        return (
            self.series.dtype == "object"
            and self.series.nunique() / self.series.count() < self.threshold
        )

    def analyze(self):
        if self.series.dtype == "category":
            return 1.0

        series_converted = pd.Categorical(self.series)
        category_ratio = self.series.nunique() / self.series.count()
        self.converted = series_converted
        return 1 - category_ratio

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.analyze()
        return self.converted if self.converted is not None else self.series

    @staticmethod
    def is_datetime_string(value):
        try:
            pd.to_datetime(value, errors="raise")
            return True
        except (ValueError, TypeError):
            return False
