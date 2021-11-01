import pandas
import pytest

from bourgault.sy import calculate_sy

TIME_SERIES_PATH = './tests/data/time_series/time_series/ahlenmoor/ahlenmoor_af_naturnah_sp.csv'


@pytest.fixture
def time_series():
    return pandas.read_csv(TIME_SERIES_PATH)


def test_calculate_sy(time_series):
    result = calculate_sy(time_series)
    print(result)

    assert result == False
