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

    filename = f"data/CLEANEDhistory-{timeframe}.csv"

    data.to_csv(filename, index=True)

    print(f"Saved resampled data to {filename}")


if __name__ == "__main__":

    data = pd.read_csv(
        "CLEANED-SPY_history.csv",
        index_col=0,
        parse_dates=True
    )

    print("original data:")
    print(data.head())

    timeframes = ["5min", "15min", "30min", "1h", "4h"]

    for timeframe in timeframes:

        resampled_data = resample_data(data, timeframe)

        save_data(
            resampled_data,
            "SPY",
            timeframe
        )