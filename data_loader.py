# Load financial data via yfinance or CSV file
# Output will be a pandas DataFrame indexed by datetime
# ['open', 'high', 'low', 'close', 'volume']

import pandas as pd

# Load data from CSV file
def load_csv(path: str, datetime_col: str = 'datetime', tz: str | None = None) -> pd.DataFrame:
  df = pd.read_csv(path)
  df.columns = [c.strip().lower() for c in df.columns]
  if datetime_col not in df.columns:
  raise ValueError(
    f"Couldn't find a '{datetime_col}' column. Found columns: {list(df.columns)}. "
    f"Pass the correct column name via datetime_col='...'"
  )
  df[datetime_col] = pd.to_datetime(df[datetime_col])
  df = df.set_index(datetime_col).sort_index()
  
  if tz:
    df.index = df.index.tz_localize(tz) if df.index.tz is None else df.index.tz_convert(tz)
    
  required = {"open", "high", "low", "close"}
  missing = required - set(df.columns)
  if missing:
    raise ValueError(f"CSV is missing required columns: {missing}")
      
  if "volume" not in df.columns:
    df["volume"] = float("NaN")
      
  return df[["open", "high", "low", "close", "volume"]]

# Load real-time data from Yahoo Finance
import yfinance as yf
def load_yfinance(pair: str = "EURUSD=X", period: str = "5y", interval: str = "1h") -> pd.DataFrame:
  raw = yf.download(pair, period=period, interval=interval, progress=False)
  if raw.empty:
    raise ValueError(f"No data returned for {pair}. Check the ticker/interval/period.")

  raw.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in raw.columns]
  raw = raw.rename(columns={"adj close": "close"})
  return raw[["open", "high", "low", "close", "volume"]]




  


  
