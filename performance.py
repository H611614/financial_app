# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 23:00:37 2025

@author: USER
"""

import numpy as np

def calculate_performance(df):
    df['Daily_Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Signal'].shift(1) * df['Daily_Return']
    cumulative_strategy = (1 + df['Strategy_Return']).cumprod()
    total_return = cumulative_strategy.iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(df)) - 1
    volatility = df['Strategy_Return'].std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility != 0 else 0
    return {
        'Total Return': total_return,
        'Annualized Return': annual_return,
        'Volatility': volatility,
        'Sharpe Ratio': sharpe_ratio
    }
