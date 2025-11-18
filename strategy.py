import pandas as pd
import numpy as np

class GoldenCross:
    def __init__(self, df: pd.DataFrame, long_period: int, short_period: int):
        self.df = df
        self.short_period = short_period
        self.long_period = long_period
        self.compute_indicators()

    def compute_indicators(self):
        #calculate moving average
        self.df["long_average"] = self.df["close"].rolling(window=self.long_period).mean()
        self.df["short_average"] = self.df["close"].rolling(window=self.short_period).mean()
        
        #filling the blanks
        self.df["long_average"]=self.df["long_average"].bfill().ffill()
        self.df["short_average"]=self.df["short_average"].bfill().ffill()

    def generate_signals(self):
        self.df["signal"] = 0

        #define crossover
        cross_up = (self.df["short_average"] > self.df["long_average"]) & \
                   (self.df["short_average"].shift(1) <= self.df["long_average"].shift(1))
        cross_down = (self.df["short_average"] < self.df["long_average"]) & \
                     (self.df["short_average"].shift(1) >= self.df["long_average"].shift(1))
        
        #Assign signals
        self.df.loc[cross_up, "signal"] = 1
        self.df.loc[cross_down, "signal"] = -1
        
        return self.df
