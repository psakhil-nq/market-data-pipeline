# Market Data Pipeline — Multi-Timeframe OHLCV for Quantitative Research

## Overview

I built this project as the market-data foundation for my quantitative trading research.

It fetches market data, validates and cleans it, resamples one base dataset into multiple timeframes, saves the final datasets, and provides a simple `get_data()` interface to access them by symbol, timeframe, and date range.

The current implementation supports SPY and QQQ.

## Motivation

I'm building toward backtesting my own futures strategies, and I wanted to solve the market-data side first.

I needed clean, consistent multi-timeframe data that I could access programmatically instead of depending completely on broker/platform charts and manually handling the data.

The goal was to build the data foundation first and use it later as the input to the backtesting project.

## Architecture — The Key Decision

The main design decision was to fetch **one base timeframe** and resample upward instead of downloading every timeframe separately.

For example:

```text
Base data
   ↓
5min
   ├── 15min
   ├── 30min
   ├── 1h
   └── 4h
```

- Using one source keeps the higher timeframes aligned to the same underlying data.

- If I downloaded 15m and 1h separately, their timestamps and bar boundaries could differ. That becomes a problem when a strategy uses multiple timeframes, because the backtest could end up comparing bars that were not actually aligned.


I also separated data generation from data access.

Generation
fetch → validate → resample → save

This runs through the generation workflow and creates the final files in data/.
 
```
Access
get_data()
   ↓
load existing CSV
   ↓
filter requested dates
   ↓
return DataFrame
```

pipeline.py is therefore an access layer, not another data-generation pipeline.


## Data Pipeline
```
Yahoo Finance
     ↓
fetch.py
     ↓
validate.py
     ↓
resample.py
     ↓
data/{symbol}-{timeframe}.csv
     ↓
pipeline.py / get_data()
     ↓
quantitative research
Metrics / Resampling
```

The OHLCV aggregation rules are:
```
Open   → first
High   → maximum
Low    → minimum
Close  → last
Volume → sum
```

These rules are used whenever a lower timeframe is converted into a higher timeframe.


## Data Quality & Validation

The validation stage checks the source data before it is resampled.
It checks:
```
Missing values
Duplicate timestamps
Timestamp ordering
Large gaps / missing intervals
```

The interval used for validation is taken into account so the gap check matches the timeframe being validated.


## Caching & Access

The generated datasets are stored locally using the symbol and timeframe in the filename:
```
data/
├── SPY-5min.csv
├── SPY-15min.csv
├── SPY-30min.csv
├── SPY-1h.csv
├── SPY-4h.csv
├── QQQ-5min.csv
├── QQQ-15min.csv
├── QQQ-30min.csv
├── QQQ-1h.csv
└── QQQ-4h.csv
```
get_data() checks the requested file, loads it, applies the requested date range, and returns the resulting DataFrame.

If the file does not exist, the pipeline raises a clear error and the generation process needs to be run first.

## Supported Symbols & Timeframes
```
Symbols
SPY
QQQ
```

These are being used as free market-data proxies for the futures research workflow.


## Timeframes
```
5min
15min
30min
1h
4h
```

## Testing

The project uses pytest.
```
Run:

python -m pytest

Current test result:

7 passed
```

The current tests mainly protects the resampling logic:
```
- OHLCV aggregation correctness
- Supported timeframe resampling
- No-NaN output
```

## Install dependencies:
```
pip install -r requirements.txt
```
## Run the generation workflow:
```
python pipeline.py

Access generated data:

from pipeline import get_data

data = get_data(
    "SPY",
    "15min",
    "2026-08-05",
    "2026-08-14"
)

print(data.head())
```

## Limitations

- SPY and QQQ are proxies, not actual ES/NQ futures data.

- Yahoo Finance is a free source and has historical intraday-data limitations.

- The current base dataset uses approximately 60 days of 5-minute data.

- This is a market-data foundation for research, not a production trading or execution system.


## Future Work

- Market-session-aware validation

- Real futures market-data source

- Integration with the strategy backtesting project

- automated tests for the generation and access layers

- additional symbols beyond SPY/QQQ, caching improvements / incremental updates


