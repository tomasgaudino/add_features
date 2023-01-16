import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from datetime import timedelta

# Set page config
st.set_page_config(layout='wide')

# Get data
df = pd.read_csv('./test_features.csv')
# Convert to datetime
df['time'] = pd.to_datetime(df['time'])

# Plot

st.title("Bollinger bands Analysis")
start_date = st.date_input("Start date", value=df['time'].min())
end_date = st.date_input("End date", value=df['time'].max()+timedelta(days=1))
memory_col = st.selectbox("Pick memory col", list(filter(lambda x: "BB_" in x and "MEMO" in x, df.columns)))
side_col = st.selectbox("Pick side col", list(filter(lambda x: "BB_" in x and "SIDE" in x, df.columns)))
down_col = st.selectbox("Pick lower bband col", list(filter(lambda x: "BBL_" in x, df.columns)))
upper_col = st.selectbox("Pick upper bband col", list(filter(lambda x: "BBU_" in x, df.columns)))

plotter_button = st.button("Plot!")
if plotter_button:
    df = df[(df['time'].dt.date >= start_date) & (df['time'].dt.date < end_date)]
    df['cross_price'] = np.where(df[side_col] != 0, df['close'] * abs(df[side_col]), np.nan)

    # Create traces
    price = go.Figure()
    price.add_trace(go.Scatter(
        x=df['time'],
        y=df['close'],
        mode='lines',
        marker_color='black',
        name='close'))
    # Cross price for long
    price.add_trace(go.Scatter(
        x=df.loc[(df[side_col] == 1), 'time'],
        y=df.loc[(df[side_col] == 1), 'cross_price'],
        mode='markers',
        marker_size=10,
        marker_color='green',
        name='Long signal'))
    # Cross price for short
    price.add_trace(go.Scatter(
        x=df.loc[(df[side_col] == -1), 'time'],
        y=df.loc[(df[side_col] == -1), 'cross_price'],
        mode='markers',
        marker_size=10,
        marker_color='red',
        name='Short signal'))

    # Lower band
    price.add_trace(go.Scatter(
        x=df['time'],
        y=df[down_col],
        mode='lines',
        marker_size=0.1,
        marker_color='violet',
        name='Lower band'))

    # Upper band
    price.add_trace(go.Scatter(
        x=df['time'],
        y=df[upper_col],
        mode='lines',
        marker_size=0.1,
        marker_color='violet',
        name='Upper band'))

    # Final adjustments
    price.update_layout(
        title="Price over time (BTC-USDT)",
        xaxis_title="Time (1min)",
        yaxis_title="Price (USDT)")

    st.plotly_chart(price, use_container_width=True)

    fig = px.histogram(df[df[side_col] != 0], x=memory_col)
    st.plotly_chart(fig, use_container_width=True)