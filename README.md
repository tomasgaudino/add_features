This project is in development stage ⌛ but it has some features that you can start using right now!


<h2>Step 1: Build you own set of indicators. There are two supported kind of indicators: crossover and intersectionable </h2>

<code> features_dict = {
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
</code>

<h2>Step 2: Choose your OHLC file</h2>

In example.py there is a .csv file containing 1min candles from btc-usdt

<h2>Step 3: Run streamlit app to visualize your features</h2>

<code>streamlit run Main_page.py</code>

<h2>Step 4: Check different indicators, i.e.: RSI, MACD, BOLLINGER</h2>

![image](https://user-images.githubusercontent.com/69804854/214636300-10beff0b-4857-41e8-a1c8-b5fc224adb60.png)

![image](https://user-images.githubusercontent.com/69804854/214636464-3399131f-4d38-4c66-9f5a-2addb49038eb.png)

![image](https://user-images.githubusercontent.com/69804854/214636520-1fc1fe23-74c9-4c1a-ba7d-3c4ecb580bf8.png)
