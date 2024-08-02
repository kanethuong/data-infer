from .base_analysis import BaseAnalysis
import pandas as pd
from api.utils import replace_null_values


class CategoryAnalysis(BaseAnalysis):
    converted = None

    def __init__(self, series, threshold=0.8):
        super().__init__(series, threshold)
        # Convert any null values in string to np.nan
        self.series = replace_null_values(series)

    def is_applicable(self) -> bool:
        # Prevent columns with too many unique values from being converted to category
        if self.series.nunique() > 50:
            return False
        # Explicitly check for datetime strings as they can be misinterpreted as categories
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

        # ratio of unique values to total values
        # the higher the ratio, the less likely the column is a category
        category_ratio = self.series.nunique() / self.series.count() 
        self.converted = series_converted
        return 1 - category_ratio # invert the ratio to get the categorical fit score

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
