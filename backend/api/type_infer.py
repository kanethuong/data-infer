import pandas as pd
import numpy as np
from .type_analysis.numeric_analysis import NumericAnalysis
from .type_analysis.datetime_analysis import DatetimeAnalysis
from .type_analysis.category_analysis import CategoryAnalysis
from .type_analysis.boolean_analysis import BooleanAnalysis
from .type_analysis.complex_analysis import ComplexAnalysis
from .type_analysis.timedelta_analysis import TimedeltaAnalysis


def get_threshold(col: pd.Series) -> float:
    c = len(col)
    if c < 100:
        return 0.6
    elif c < 1000:
        return 0.7
    return 0.8


def infer_data_types(col: pd.Series) -> np.dtype:
    series = col
    threshold = get_threshold(series)
    result_list = []

    all_analyses = [
        NumericAnalysis,
        DatetimeAnalysis,
        CategoryAnalysis,
        BooleanAnalysis,
        ComplexAnalysis,
        TimedeltaAnalysis,
    ]

    analyses = map(lambda a: a(series=series, threshold=threshold), all_analyses)
    for analysis in analyses:
        analysis_name = analysis.__class__.__name__
        if analysis_name == DatetimeAnalysis.__name__:
            continue
        run_analysis(analysis, threshold, result_list)

    # Run DatetimeAnalysis last
    if not result_list:
        print("No type found. Running DatetimeAnalysis")
        datetime_threshold = 0.1
        analysis = DatetimeAnalysis(series=series, threshold=datetime_threshold)
        run_analysis(analysis, datetime_threshold, result_list)

    # Determine the best type with the highest ratio
    result_list.sort(
        key=lambda x: (
            max(x.analyze()) if isinstance(x.analyze(), tuple) else x.analyze()
        ),
        reverse=True,
    )

    if result_list:
        print(f"Found {len(result_list)} types. Best type: {result_list[0].get_type()}")
    else:
        print("No type found")

    return result_list[0].get_type() if result_list else col.dtype


def run_analysis(analysis, threshold, results_list):
    print(
        f"Trying analysis {analysis.__class__.__name__} for column {analysis.series.name}"
    )

    try:
        if not analysis.is_applicable():
            print(f"Analysis {analysis.__class__.__name__} not applicable")
            return
        analysis_result = analysis.analyze()

        if isinstance(analysis_result, tuple):
            max_ratio = max(analysis_result)
        else:
            max_ratio = analysis_result

        if max_ratio >= threshold:
            results_list.append(analysis)
            print(
                f"Analysis {analysis.__class__.__name__} with ratio {analysis.analyze()} applicable"
            )
        else:
            print(
                f"Analysis {analysis.__class__.__name__} not applicable (ratio {analysis.analyze()})"
            )
    except Exception as e:
        print(f"Analysis {analysis.__class__.__name__} failed with error {e}")
