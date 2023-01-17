import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta

# Set page config
st.set_page_config(layout='wide')

# Get data
df = pd.read_csv('./test_features.csv')
# Convert to datetime
df['time'] = pd.to_datetime(df['time'])


st.title("MACD Analysis")
start_date = st.date_input("Start date", value=df['time'].min())
end_date = st.date_input("End date", value=df['time'].max()+timedelta(days=1))
macd_col = st.selectbox("Pick MACD col", list(filter(lambda x: "MACD_" in x and "CROSS" not in x and "ALPHA" not in x and "VALUE" not in x and "SIDE" not in x, df.columns)))
signal_col = st.selectbox("Pick Signal col", list(filter(lambda x: "MACDs_" in x, df.columns)))
cross_col = st.selectbox("Pick cross col", list(filter(lambda x: "MACD_" in x and "CROSS" in x, df.columns)))
alpha_col = st.selectbox("Pick alpha col", list(filter(lambda x: "MACD_" in x and "ALPHA" in x, df.columns)))
value_col = st.selectbox("Pick value col", list(filter(lambda x: "MACD_" in x and "VALUE" in x, df.columns)))
side_col = st.selectbox("Pick side col", list(filter(lambda x: "MACD_" in x and "SIDE" in x, df.columns)))

plotter_button = st.button("Plot!")
if plotter_button:

    df = df[(df['time'].dt.date >= start_date) & (df['time'].dt.date < end_date)]
    df['cross_timestamp'] = np.where(df[cross_col] != df[cross_col].shift(1), 1, np.nan)
    df['cross_price'] = df['close'] * df['cross_timestamp']
    # Create traces
    price = go.Figure()
    price.add_trace(go.Scatter(
        x=df['time'],
        y=df['close'],
        mode='lines',
        name='close'))
    price.add_trace(go.Scatter(
        x=df.loc[(df[side_col] == 1) & (df[cross_col] != 0), 'time'],
        y=df.loc[(df[side_col] == 1) & (df[cross_col] != 0), 'cross_price'],
        mode='markers',
        marker_size=abs(df.loc[(df[side_col] == 1), value_col] * 100),
        marker_color='green',
        name='Long signal'))
    price.add_trace(go.Scatter(
        x=df.loc[(df[side_col] == -1) & (df[cross_col] != 0), 'time'],
        y=df.loc[(df[side_col] == -1) & (df[cross_col] != 0), 'cross_price'],
        mode='markers',
        marker_size=abs(df.loc[(df[side_col] == -1), value_col] * 100),
        marker_color='red',
        name='Short signal'))

    price.update_layout(
        title="Price over time (BTC-USDT)",
        xaxis_title="Time (1min)",
        yaxis_title="Price (USDT)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df[macd_col],
        mode='lines',
        name='MACD'))
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df[signal_col],
        mode='lines',
        name='Signal'))
    fig.add_trace(go.Scatter(
        x=df.loc[df[cross_col] == 1, 'time'],
        y=df.loc[df[cross_col] == 1, macd_col],
        mode='markers',
        marker_color='black',
        name='Intersection points'))


    fig.update_layout(
        title="Intersection analysis",
        xaxis_title="Time (1min)",
        yaxis_title="Value")

    st.plotly_chart(price, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df.loc[df[cross_col] > 0, [macd_col, signal_col, value_col, side_col, alpha_col, cross_col]])
    st.text(df.loc[df[cross_col] > 0, [macd_col, signal_col, value_col, side_col, alpha_col, cross_col]].dtypes)