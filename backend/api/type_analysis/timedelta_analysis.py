from .base_analysis import BaseAnalysis
import pandas as pd
from api.utils import replace_null_values


class TimedeltaAnalysis(BaseAnalysis):
    converted = None

    def __init__(self, series, threshold=0.8):
        super().__init__(series, threshold)
        self.series = replace_null_values(series)

    def is_applicable(self) -> bool:
        sample_data = self.series.head()
        while sample_data.isna().all() and len(sample_data) < len(self.series):
            sample_data = self.series.head(len(sample_data) * 2)

        converted_data = pd.to_timedelta(sample_data, errors="coerce")
        return converted_data.notna().any()

    def analyze(self):
        series_converted = pd.to_timedelta(self.series, errors="coerce")
        timedelta_ratio = self.series.apply(series_converted).notna().mean()
        self.converted = series_converted
        return timedelta_ratio

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.analyze()
        return self.converted if self.converted is not None else self.series
