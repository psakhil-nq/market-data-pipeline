import pandas as pd
import pytest
from resample import resample_data

def test_five_minute_ohlcv():

    index = pd.date_range(
        "2026-01-01 09:30",
        periods=5,
        freq="min"
    )

    data = pd.DataFrame({
        "Open": [100, 101, 102, 103, 104],
        "High": [101, 103, 104, 105, 106],
        "Low": [99, 100, 101, 102, 103],
        "Close": [100.5, 102, 103.5, 104, 105],
        "Volume": [100, 200, 300, 400, 500],
    }, index=index)

    result = resample_data(data, timeframe="5min")

    assert result.iloc[0]["Open"] == 100
    assert result.iloc[0]["High"] == 106
    assert result.iloc[0]["Low"] == 99
    assert result.iloc[0]["Close"] == 105
    assert result.iloc[0]["Volume"] == 1500

@pytest.mark.parametrize("timeframe", ["5min", "15min" , "30min", "1h" , "4h"])
def test_supported_timeframes(timeframe):

    index = pd.date_range(
        "2026-01-01 09:30",
        periods=240,
        freq="min"
    )

    data = pd.DataFrame({
        "Open": range(240),
        "High": range(1, 241),
        "Low":  range(240),
        "Close": range(240),
        "Volume": [100] * 240,
    }, index=index)

    result = resample_data(data, timeframe)
    assert not result.empty

def test_no_nan_rows():

    index = pd.date_range(
        "2026-01-01 09:30",
        periods=240,
        freq="min"
    )

    data = pd.DataFrame({
        "Open":range(240),
        "High": range (1,241),
        "Low": range(240),
        "Close": range(240),
        "Volume":[100] * 240, 
    }, index=index)

    result = resample_data(data, timeframe="5min")

    assert not result[["Open","High","Low","Close","Volume"]].isna().any().any()