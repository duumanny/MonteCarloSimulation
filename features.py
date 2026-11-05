# Convert data into a feature matrix for the machine learning model, build prediction target:
# Will price be Higher or Lower (1/0), N bars ahead

import numpy as np
import pandas as pd
import ta 

def build_features(df: pd.DataFrame, horizon: int = 5) -> pd.DataFrame:
  out = df.copy()

  # Basic returns / Volatility
  out["ret_1"] = out["close"].pct_change(1)
  out["ret_3"] = out["close"].pct_change(3)
  out["ret_5"] = out["close"].pct_change(5)
  out["ret_10"] = out["close"].pct_change(10)
  out["volatility_10"] = out["ret_1"].rolling(10).std()
  out["volatility_30"] = out["ret_1"].rolling(30).std()

  # Trend Indicators 
  out["sma_10"] = ta.trend.sma_indicator(out["close"], window=10)
  out["sma_50"] = ta.trend.sma_indicator(out["close"], window=50)
  out["ema_10"] = ta.trend.ema_indicator(out["close"], window=10)
  out["ema_50"] = ta.trend.ema_indicator(out["close"], window=50)
  out["sma_diff"] = (out["sma_10"] - out["sma_50"]) / out["close"]
  out["macd"] = ta.trend.macd(out["close"])
  out["macd_signal"] = ta.trend.macd_signal(out["close"])
  out["macd_diff"] = ta.trend.macd_diff(out["close"])
  out["adx"] = ta.trend.adx(out["high"], out["low"], out["close"], window=14)


  # Momentum / Oscillators
  out["rsi_14"] = ta.momentum.rsi(out["close"], window=14)
  out["stoch_k"] = ta.momentum.stoch(out["high"], out["low"], out["close"])
  out["williams_r"] = ta.momentum.williams_r(out["high"], out["low"], out["close"])

  
  # Volatility bands
  bb = ta.volatility.BollingerBands(out["close"], window=20, window_dev=2)
  out["bb_pct"] = bb.bollinger_pband()
  out["bb_width"] = bb.bollinger_wband()
  out["atr_14"] = ta.volatility.average_true_range(out["high"], out["low"], out["close"], window=14)


  # Candle structure
  out["body"] = (out["close"] - out["open"]) / out["open"]
  out["upper_wick"] = (out["high"] - out[["open", "close"]].max(axis=1)) / out["open"]
  out["lower_wick"] = (out[["open", "close"]].min(axis=1) - out["low"]) / out["open"]


  # Time of Day / Session features
  out["hour"] = out.index.hour
  out["dow"] = out.index.dayofweek
  out["hour_sin"] = np.sin(2 * np.pi * out["hour"] / 24)
  out["hour_cos"] = np.cos(2 * np.pi * out["hour"] / 24)


  # Target
  future_close = out["close"].shift(-horizon)
  out["future_return"] = (future_close - out["close"]) / out["close"]
  out["target"] = (out["future_return"] > 0).astype(int)

  out = out.dropna()
  return out

FEATURE_COLUMNS = [
    "ret_1", "ret_3", "ret_5", "ret_10",
    "volatility_10", "volatility_30",
    "sma_diff", "macd", "macd_signal", "macd_diff", "adx",
    "rsi_14", "stoch_k", "williams_r",
    "bb_pct", "bb_width", "atr_14",
    "body", "upper_wick", "lower_wick",
    "hour_sin", "hour_cos", "dow",
]
