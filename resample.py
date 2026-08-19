import pandas as pd

def resample_data(data, timeframe):

    ohlcv_rules = {
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }

    resampled_data = data.resample(timeframe).agg(ohlcv_rules)

    resampled_data = resampled_data[
        resampled_data["Open"].notna()
    ]

    return resampled_data


def save_data(data, symbol, timeframe):

    filename = f"data/{symbol}-{timeframe}.csv"

    data.to_csv(filename, index=True)

    print(f"Saved resampled data to {filename}")
