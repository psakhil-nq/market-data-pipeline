import pandas as pd
from pathlib import Path
from validate import validate_data
from fetch import fetch_data, INTERVAL
from resample import resample_data, save_data

def load_data(filename):
    data = pd.read_csv(filename, index_col=0, parse_dates=True)
    return data
    
def get_data(symbol, timeframe, start_date, end_date):

    valid_timeframes = ["5min", "15min", "30min", "1h", "4h"]
    if timeframe not in valid_timeframes:
        raise ValueError(f"Invalid timeframe. Valid options are: {valid_timeframes}")
    valid_symbols = ["SPY", "QQQ"]
    if symbol not in valid_symbols:
        raise ValueError(f"Invalid symbol. Valid options are: {valid_symbols}")

    filename = Path(f"data/{symbol}-{timeframe}.csv")
    if filename.exists():
        data = load_data(filename)
    else:
        raise ValueError("No data Available For Requested Timeframe")
    
    data = data.loc[start_date:end_date]

    return data

def gen_all_tf(symbol):
   
   timeframes = ["5min", "15min", "30min", "1h", "4h"]
   new_data = fetch_data(symbol)

   validation_result = validate_data(new_data, INTERVAL)
   if not validation_result["passed"]:
       raise ValueError("Downloaded Data Failed Validation")

   for timeframe in timeframes:
       data = resample_data(new_data, timeframe)
       save_data(data,symbol,timeframe)

if __name__ == "__main__":
     symbol = input("Enter Symbol , (eg. SPY,QQQ): ").upper()
     gen_all_tf(symbol)