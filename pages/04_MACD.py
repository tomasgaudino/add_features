import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(layout='wide')

# Get data
df = pd.read_csv('eth_1min_hma_w_angles.csv')
# Convert to datetime
df['time'] = pd.to_datetime(df['time'])
df['cross_timestamp'] = np.where(df['cross'] != df['cross'].shift(1), 1, np.nan)
df['cross_price'] = df['close'] * df['cross_timestamp']
# Reduce number of rows (too heavy)
df = df[df['time'].dt.month > 9]


st.title("Intersection models")
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
        x=df.loc[(df['side'] == 'long') & ~(df['cross'].isna()), 'time'],
        y=df.loc[(df['side'] == 'long') & ~(df['cross'].isna()), 'cross_price'],
        mode='markers',
        marker_size=abs(df.loc[df['cross'] == 1, 'alpha'])+abs(df.loc[df['cross'] == 1, 'beta'])*100,
        marker_color='green',
        name='Long signal'))
    price.add_trace(go.Scatter(
        x=df.loc[(df['side'] == 'short') & ~(df['cross'].isna()), 'time'],
        y=df.loc[(df['side'] == 'short') & ~(df['cross'].isna()), 'cross_price'],
        mode='markers',
        marker_size=abs(df.loc[df['cross'] == 1, 'alpha'])+abs(df.loc[df['cross'] == 1, 'beta'])*100,
        marker_color='red',
        name='Short signal'))

    price.update_layout(
        title="Price over time (ETH-USDT)",
        xaxis_title="Time (1min)",
        yaxis_title="Price (USDT)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['HMA'],
        mode='lines',
        name='MACD'))
    fig.add_trace(go.Scatter(
        x=df.loc[df['cross'] == 1, 'time'],
        y=df.loc[df['cross'] == 1, 'HMA'],
        mode='markers',
        marker_color='black',
        name='Intersection points'))
    # fig.add_trace(go.Bar(
    #     x=df.loc[df['side'] == 'short', 'time'],
    #     y=-df.loc[df['side'] == 'short', 'alpha'],
    #     marker_color='red',
    #     name='Short signal'# marker color can be a single color value or an iterable
    # ))
    # fig.add_trace(go.Bar(
    #     x=df.loc[df['side'] == 'long', 'time'],
    #     y=df.loc[df['side'] == 'long', 'beta'],
    #     marker_color='green',
    #     name='Long signal'
    # ))

    fig.update_layout(
        title="Intersection analysis",
        xaxis_title="Time (1min)",
        yaxis_title="Value")

    st.plotly_chart(price, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df[~df['side'].isna()])