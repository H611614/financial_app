# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 23:01:58 2025

@author: USER
"""

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from indicators import calculate_ma, calculate_rsi, calculate_bollinger_bands, calculate_macd
from strategies import ma_crossover_strategy, rsi_strategy, optimize_ma_strategy
from performance import calculate_performance

st.title("期末作業：金融資料視覺化與程式交易平台")

# 上傳CSV
uploaded_file = st.sidebar.file_uploader("請上傳CSV檔案", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    st.sidebar.header("技術指標設定")
    if st.sidebar.checkbox("顯示移動平均(MA)"):
        ma_period = st.sidebar.slider("MA週期", 5, 50, 20)
        df = calculate_ma(df, ma_period)
    if st.sidebar.checkbox("顯示RSI"):
        df = calculate_rsi(df)
    if st.sidebar.checkbox("顯示布林通道"):
        df = calculate_bollinger_bands(df)
    if st.sidebar.checkbox("顯示MACD"):
        df = calculate_macd(df)

    st.header("K線圖與技術指標")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="K線"))
    if f"MA_{ma_period}" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[f"MA_{ma_period}"], mode='lines', name=f"MA_{ma_period}"))
    if 'BB_upper' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], line=dict(dash='dot'), name="BB Upper"))
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], line=dict(dash='dot'), name="BB Lower"))
    st.plotly_chart(fig)

    st.header("策略回測")
    strategy = st.selectbox("選擇策略", ["MA交叉", "RSI"])
    if strategy == "MA交叉":
        short = st.number_input("短期均線", 5, 50, 10)
        long = st.number_input("長期均線", 10, 200, 50)
        df = ma_crossover_strategy(df, short, long)
    elif strategy == "RSI":
        rsi_buy = st.number_input("RSI買進門檻", 10, 50, 30)
        rsi_sell = st.number_input("RSI賣出門檻", 50, 90, 70)
        df = rsi_strategy(df, rsi_buy, rsi_sell)

    st.line_chart((1 + df['Signal'].shift(1) * df['Close'].pct_change()).cumprod())

    st.header("績效指標")
    perf = calculate_performance(df)
    st.write(perf)

    if st.button("執行MA參數最佳化"):
        short_range = range(5, 21)
        long_range = range(30, 101)
        best_params, best_df = optimize_ma_strategy(df, short_range, long_range)
        st.write(f"最佳參數: 短期={best_params[0]}, 長期={best_params[1]}")
