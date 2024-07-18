import pandas as pd
import numpy as np


class BaseAnalysis:
    def __init__(self, series: pd.Series, threshold=0.8):
        self.series = series
        self.threshold = threshold

    def is_applicable(self) -> bool:
        return True

    def convert(self):
        return NotImplementedError

    def get_type(self) -> np.dtype:
        raise NotImplementedError

    def analyze(self):
        raise NotImplementedError
