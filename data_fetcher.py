import yfinance as yf
import pandas as pd

def fetch_from_yf(symbol: str, period="5y", interval="1d"):
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
    df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
    return df
