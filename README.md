<h1>Experimental Project</h1>
<p>This project is still in its experimental phase, and while we are working hard to improve it, it may still contain bugs.

We believe this project has great potential, and we are committed to continuously improving it. If you'd like to help us on this journey, we'd love for you to collaborate with us! Whether you're a seasoned developer or just starting out, there's a place for you here.

Please feel free to open issues for bug reports or feature requests, and we'll do our best to address them as soon as possible. We welcome all contributions, from small bug fixes to major feature enhancements. Let's build something amazing together!</p>

<h1>OHLC Features Transformation Project</h1>
<p>This project is focused on transforming an [Open, High, Low, Close (OHLC)] financial time series data into meaningful features using a customizable features_dict. The features_dict allows you to define different technical indicators and configurations for each indicator.

The core class, OHLCFeatures, accepts an OHLC data and the features_dict as input and returns the computed features for each indicator. The computed features can be used for further analysis and trading strategy development. The project leverages the power of the pandas_ta library for calculating technical indicators.</p>

<h2>Usage</h2>
<p>The features_dict is a dictionary that consists of two keys, crossover and intersection. The crossover key holds configurations for crossover indicators such as Relative Strength Index (RSI) and Bollinger Bands (BBands), while the intersection key holds configurations for intersection indicators such as Moving Average Convergence Divergence (MACD).

Here is an example of a usage:</p>
<pre>import pandas as pd
from add_features.generate import Features, PositionSide

df = pd.read_csv('data/btc_1min.csv')

features_dict = {
    'crossover': {
        'rsi': [
            {'upper_thold': 70, 'upper_side': PositionSide.SHORT, 'down_thold': 30, 'down_side': PositionSide.LONG, 'config': {'length': 14}},
            {'upper_thold': 65, 'upper_side': PositionSide.SHORT, 'down_thold': 35, 'down_side': PositionSide.LONG, 'config': {'length': 21}},
            {'upper_thold': 60, 'upper_side': PositionSide.SHORT, 'down_thold': 40, 'down_side': PositionSide.LONG, 'config': {'length': 28}},
        ],
        'bbands': [
            {'upper_side': PositionSide.SHORT, 'down_side': PositionSide.LONG, 'config': {'length': 20}},
            {'upper_side': PositionSide.SHORT, 'down_side': PositionSide.LONG, 'config': {'length': 30, 'mamode':'t3'}},
        ]
    },
    'intersection': {
        'macd': [
            {'series1_breakup_side': PositionSide.LONG, 'series2_breakup_side': PositionSide.SHORT, 'config': {"fast": 12, "slow": 26, "signal": 9}},
            {'series1_breakup_side': PositionSide.LONG, 'series2_breakup_side': PositionSide.SHORT, 'config': {"fast": 15, "slow": 30, "signal": 12}},
            {'series1_breakup_side': PositionSide.LONG, 'series2_breakup_side': PositionSide.SHORT, 'config': {"fast": 18, "slow": 34, "signal": 15}},
        ]
    }
}
ft = Features()
features_df = ft.add_features(df, features_dict)
features_df.to_csv('test_features.csv')</pre>

<h2>Visualize</h2>
<p>Every feature generated from the project can be visualized and tested in a Streamlit dashboard. Currently, only MACD, RSI and Bollinger Bands are supported, but the number of supported indicators can keep growing. You can participate and help the project to keep growing too!

Some screenshots:</p>

![image](https://user-images.githubusercontent.com/69804854/214636300-10beff0b-4857-41e8-a1c8-b5fc224adb60.png)

![image](https://user-images.githubusercontent.com/69804854/214636464-3399131f-4d38-4c66-9f5a-2addb49038eb.png)

![image](https://user-images.githubusercontent.com/69804854/214636520-1fc1fe23-74c9-4c1a-ba7d-3c4ecb580bf8.png)
