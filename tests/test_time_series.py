import pandas
import pytest
from peatland_time_series.time_series import read_time_series

TIME_SERIES_PATH = './tests/data/time_series/time_series/ahlenmoor/ahlenmoor_af_naturnah_sp.csv'
BAD_TIME_SERIES_PATH = './tests/data/time_series/time_series/bad-time-series.csv'
EXPECTED_COLUMNS = ['data_wtd', 'data_prec']
EXPECTED_INDEX = 'date'

def test_read_time_series():
    result = read_time_series(TIME_SERIES_PATH)

    assert isinstance(result, pandas.DataFrame)
    for expected_column in EXPECTED_COLUMNS:
        assert expected_column in result.columns, f'Missing "{expected_column}" column in result'

    assert result.index.name == EXPECTED_INDEX
    assert pandas.api.types.is_datetime64_dtype(result.index)


def test_read_bad_time_series():
    with pytest.raises(ValueError):
        read_time_series(BAD_TIME_SERIES_PATH)

