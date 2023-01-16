import pandas as pd
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
features_df.to_csv('test_features.csv')