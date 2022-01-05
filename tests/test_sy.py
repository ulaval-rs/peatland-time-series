import numpy
import pandas
import pytest

from peatland_time_series.sy import calculate_sy, read_sy

TIME_SERIES_PATH = './tests/data/time_series/time_series/ahlenmoor/ahlenmoor_af_naturnah_sp.csv'
SY_PATH = './tests/data/sy.csv'
EXPECTED_COLUMNS = ['date_beginning', 'date_ending', 'precipitation_sum', 'max_wtd', 'min_wtd',
                    'durations', 'intensities', 'delta_h', 'depth', 'sy', 'idx_max', 'idx_min',
                    'accuracy_mean', 'accuracy_std']


@pytest.fixture
def time_series():
    return pandas.read_csv(TIME_SERIES_PATH)


@pytest.fixture
def expected_result():
    return pandas.read_csv(SY_PATH)


def test_calculate_sy(time_series, expected_result):
    result = calculate_sy(time_series)

    for expected_column in EXPECTED_COLUMNS:
        assert expected_column in result.columns

    for i, j in zip(expected_result['sy'].values, result['sy'].values):
        if numpy.isnan(i) and numpy.isnan(j):
            continue

        if numpy.isinf(i) and numpy.isinf(j):
            continue

        assert abs(i - j) < 1e-15  # Ignoring numerical difference (~1e-16)


def test_read_sy():
    result = read_sy(SY_PATH)

    for expected_column in EXPECTED_COLUMNS:
        assert expected_column in result.columns, f'Missing "{expected_column}" column in result'

    assert pandas.api.types.is_datetime64_dtype(result['date_beginning'])
    assert pandas.api.types.is_datetime64_dtype(result['date_ending'])
    assert pandas.api.types.is_datetime64_dtype(result['idx_min'])
    assert pandas.api.types.is_datetime64_dtype(result['idx_max'])
