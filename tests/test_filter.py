from typing import Dict

import pandas
import pytest

from peatland_time_series.filter import filter_sy

SY_PATH = './tests/data/sy.csv'


@pytest.fixture
def sy():
    return pandas.read_csv(SY_PATH)


@pytest.mark.parametrize('filters, tolerate_intervals', [
    ({
         'precipitation_sum_min': 2.0,
         'precipitation_sum_max': 7.0
     }, {
         'precipitation_sum': (2.0, 7.0)
     }),
    ({
         'sy_min': 0.2,
         'sy_max': 0.25
     }, {
         'sy': (0.2, 0.25)
     }),
])
def test_filter(sy: pandas.DataFrame, filters: Dict, tolerate_intervals: Dict):
    result = filter_sy(sy, **filters)

    for key, value in tolerate_intervals.items():
        min_tolerance, max_tolerance = value

        valid_check = (result[key] > min_tolerance) & (result[key] < max_tolerance)

        assert valid_check.all(), f"Some of the \"{key}\" values were not in the tolerances [{min_tolerance}, {max_tolerance}]."


@pytest.mark.parametrize('filters, tolerate_intervals', [
    ({
         'precipitation_sum_min': 2.0,
         'precipitation_sum_max': 7.0
     }, {
         'precipitation_sum': (2.0, 6.0)
     }),
    ({
         'sy_min': 0.2,
         'sy_max': 0.25
     }, {
         'sy': (0.2, 0.21)
     }),
])
def test_filter_with_expected_wrong_tolerances(sy: pandas.DataFrame, filters: Dict, tolerate_intervals: Dict):
    result = filter_sy(sy, **filters)

    for key, value in tolerate_intervals.items():
        min_tolerance, max_tolerance = value

        valid_check = (result[key] > min_tolerance) & (result[key] < max_tolerance)

        assert not valid_check.all()
