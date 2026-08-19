import yfinance as yf

INTERVAL = "5m"


def fetch_data(symbol):

    ticker = yf.Ticker(symbol)

    data = ticker.history(
        period="60d",
        interval=INTERVAL
    )

    data = data.drop(
        ["Dividends", "Stock Splits", "Capital Gains"],
        axis=1
    )

    return data


if __name__ == "__main__":

    symbol = input("Enter Symbol (eg.SPY,QQQ): ").upper()
    data = fetch_data(symbol)

    data.to_csv(
        f"RAW-{symbol}_history.csv",
        index=True
    )

    print(f"Historical data saved to RAW-{symbol}_history.csv")
    print(data.columns)
    print(data.shape)