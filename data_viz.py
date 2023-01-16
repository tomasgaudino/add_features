import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

df = pd.read_csv('test_features.csv')

# Convert to datetime
df['time'] = pd.to_datetime(df['time'])

# Plot
df['cross_price'] = np.where(df['RSI_14_SIDE'] != 0, df['close'] * abs(df['RSI_14_SIDE']), np.nan)

st.title("Crossover models")
start_date = st.date_input("Start date", value=df['time'].min())
end_date = st.date_input("End date", value=df['time'].max())

plotter_button = st.button("Plot!")
if plotter_button:
    df = df[(df['time'].dt.date >= start_date) & (df['time'].dt.date < end_date)]
    # Create traces
    price = go.Figure()
    price.add_trace(go.Scatter(
        x=df['time'],
        y=df['close'],
        mode='lines',
        name='close'))
    price.add_trace(go.Scatter(
        x=df.loc[(df['RSI_14_SIDE'] == 1), 'time'],
        y=df.loc[(df['RSI_14_SIDE'] == 1), 'cross_price'],
        mode='markers',
        # marker_size=df['rsi_memory'],
        marker_color='green',
        name='Long signal'))
    price.add_trace(go.Scatter(
        x=df.loc[(df['RSI_14_SIDE'] == -1), 'time'],
        y=df.loc[(df['RSI_14_SIDE'] == -1), 'cross_price'],
        mode='markers',
        # marker_size=df['rsi_memory'],
        marker_color='red',
        name='Short signal'))
    price.update_layout(
        title="Price over time (BTC-USDT)",
        xaxis_title="Time (1min)",
        yaxis_title="Price (USDT)")

    st.plotly_chart(price, use_container_width=True)

    # fig = px.histogram(df[df['rsi_side']!=0], x="rsi_memory")
    fig = px.histogram(df, x="RSI_14_MEMO")
    st.plotly_chart(fig, use_container_width=True)