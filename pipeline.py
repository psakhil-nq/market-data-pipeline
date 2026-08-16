import pandas as pd
from pathlib import Path
from validate import validate_data
from fetch import fetch_data
from resample import resample_data, save_data

def load_data(filename):
    data = pd.read_csv(filename, index_col=0, parse_dates=True)
    return data
    
def get_data(symbol, timeframe, start_date, end_date):

    valid_timeframes = ["5min", "15min", "30min", "1h", "4h"]
    if timeframe not in valid_timeframes:
        raise ValueError(f"Invalid timeframe. Valid options are: {valid_timeframes}")
    valid_symbols = ["SPY"]
    if symbol not in valid_symbols:
        raise ValueError(f"Invalid symbol. Valid options are: {valid_symbols}")

    filename = Path(f"data/CLEANEDhistory-{timeframe}.csv")
    if filename.exists():
        data = load_data(filename)
    else:
         raw_data = fetch_data(symbol)

         validation_result = validate_data(raw_data)

         if not validation_result["passed"]:
             raise ValueError("Downloaded data failed validation")

         data = resample_data(raw_data, timeframe)

         save_data(data, symbol, timeframe)
    
         data = data.loc[start_date:end_date]
         validation_result = validate_data(data)

    return data

data = get_data("SPY", "5min", "2026-08-05", "2026-08-14")
print(data.head())
print(data.tail())