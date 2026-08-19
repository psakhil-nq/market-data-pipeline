import yfinance as yf


def fetch_data(symbol):

    ticker = yf.Ticker(symbol)

    data = ticker.history(
        period="60d",
        interval="5m"
    )

    data = data.drop(
        ["Dividends", "Stock Splits", "Capital Gains"],
        axis=1
    )

    return data


if __name__ == "__main__":

    data = fetch_data("SPY")

    data.to_csv(
        "CLEANED-SPY_history.csv",
        index=True
    )

    print("Historical data saved to CLEANED-SPY_history.csv")
    print(data.columns)
    print(data.shape)