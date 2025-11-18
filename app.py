import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import fetch_from_yf
from strategy import GoldenCross
from backtester import Backtester

# Title
st.title("Trading Strategy Backtest Dashboard")

# User input-
symbol = st.text_input("Enter Stock Symbol", "AAPL")



period = st.selectbox(
    "Select Period:",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    index=6  # default "5y"
)

interval = st.selectbox(
    "Select Interval:",
    ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", 
     "1d", "5d", "1wk", "1mo", "3mo"],
    index=8  # default "1d"
)


if st.button("Run Backtest"):
    df = fetch_from_yf(symbol, period, interval)
    strategy = GoldenCross(df, long_period=200, short_period=50)
    df = strategy.generate_signals()

    backtester = Backtester(df)
    final_value, trades = backtester.run()

    st.subheader(f"Final Portfolio Value: ${final_value:,.2f}")

    # Show trades table
    st.dataframe(pd.DataFrame(trades, columns=["Action", "Price", "Date"]))

    # Plot price + signals
    fig, ax = plt.subplots()
    ax.plot(df.index, df["close"], label="Price")
    ax.plot(df.index, df["long_average"], label="Long MA")
    ax.plot(df.index, df["short_average"], label="Short MA")

    buy_signals = df[df["signal"] == 1]
    sell_signals = df[df["signal"] == -1]
    ax.scatter(buy_signals.index, buy_signals["close"], marker="^", color="green", label="Buy", alpha=1)
    ax.scatter(sell_signals.index, sell_signals["close"], marker="v", color="red", label="Sell", alpha=1)

    ax.legend()
    st.pyplot(fig)
