from datetime import datetime
from typing import Dict

import pandas
import pytest
from peatland_time_series.filter import filter_sy
from peatland_time_series.sy import read_sy

SY_PATH = './tests/data/sy.csv'


@pytest.fixture
def sy():
    return read_sy(SY_PATH)


@pytest.mark.parametrize('filters, tolerances', [
    ({
         'precipitation_sum_min': 2.0,
         'precipitation_sum_max': 7.0
     }, {
         'precipitation_sum': (2.0, 7.0)
     }),
    ({
         'sy_min': 0.2,
         'sy_max': 0.25,
         'date_beginning_min': pandas.Timestamp('2011-08-03 22:00:00'),
         'date_beginning_max': pandas.Timestamp('2011-08-31 06:00:00'),
         'date_ending_min': pandas.Timestamp('2011-08-11 04:00:00'),
         'date_ending_max': pandas.Timestamp('2011-08-30 01:00:00'),
     }, {
         'sy': (0.2, 0.25),
         'date_beginning': (pandas.Timestamp('2011-08-03 22:00:00'), pandas.Timestamp('2011-08-31 06:00:00')),
         'date_ending': (pandas.Timestamp('2011-08-11 04:00:00'), pandas.Timestamp('2011-08-30 01:00:00')),
     }),
])
def test_filter(sy: pandas.DataFrame, filters: Dict, tolerances: Dict):
    result = filter_sy(sy, **filters)

    for key, value in tolerances.items():
        min_tolerance, max_tolerance = value

        valid_check = (result[key] >= min_tolerance) & (result[key] <= max_tolerance)

        assert valid_check.all(), f"Some of the \"{key}\" values were not in the tolerances [{min_tolerance}, {max_tolerance}]."


@pytest.mark.parametrize('filters, tolerances', [
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
def test_filter_with_expected_wrong_tolerances(sy: pandas.DataFrame, filters: Dict, tolerances: Dict):
    result = filter_sy(sy, **filters)

    for key, value in tolerances.items():
        min_tolerance, max_tolerance = value

        valid_check = (result[key] > min_tolerance) & (result[key] < max_tolerance)

        assert not valid_check.all()
