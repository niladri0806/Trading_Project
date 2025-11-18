from data_fetcher import fetch_from_yf
from strategy import GoldenCross
from backtester import Backtester

df = fetch_from_yf("APLD", period="5y")
strategy = GoldenCross(df, long_period=200, short_period=50)
df = strategy.generate_signals()

backtester = Backtester(df)
final_value, trades = backtester.run()


df.to_html("Trade_output.html", index=False)
print("Final Portfolio Value:", final_value)
print("Trades:", trades)
