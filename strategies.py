# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 22:59:23 2025

@author: USER
"""

from indicators import calculate_ma, calculate_rsi
import numpy as np
from itertools import product

def ma_crossover_strategy(df, short_window=10, long_window=50):
    df = calculate_ma(df, short_window)
    df = calculate_ma(df, long_window)
    df['Signal'] = 0
    df.loc[df[f"MA_{short_window}"] > df[f"MA_{long_window}"], 'Signal'] = 1
    df.loc[df[f"MA_{short_window}"] < df[f"MA_{long_window}"], 'Signal'] = -1
    return df

def rsi_strategy(df, rsi_buy=30, rsi_sell=70):
    df = calculate_rsi(df)
    df['Signal'] = 0
    df.loc[df['RSI'] < rsi_buy, 'Signal'] = 1
    df.loc[df['RSI'] > rsi_sell, 'Signal'] = -1
    return df

def optimize_ma_strategy(df, short_range, long_range):
    best_result = None
    best_params = (0, 0)
    best_return = -np.inf
    for short, long in product(short_range, long_range):
        if short >= long:
            continue
        test_df = ma_crossover_strategy(df.copy(), short, long)
        result = test_df['Signal'].shift(1) * df['Close'].pct_change()
        total_return = result.sum()
        if total_return > best_return:
            best_return = total_return
            best_params = (short, long)
            best_result = test_df.copy()
    return best_params, best_result
