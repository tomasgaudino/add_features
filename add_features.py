import pandas_ta as ta
import pandas as pd
import numpy as np
from enum import Enum


class PositionSide(Enum):
    LONG = 1
    SHORT = -1
    NEUTRAL = 0


def crossover(
        base: pd.Series,
        upper_thold: pd.Series,
        upper_side: PositionSide,
        down_thold: pd.Series,
        down_side: PositionSide):
    df = pd.concat([base, upper_thold, down_thold], axis=1)

    df['side'] = np.where(base < down_thold,
                          down_side,
                          np.where(base > upper_thold,
                                   upper_side,
                                   PositionSide.NEUTRAL))

    df['memory'] = df.groupby((df['side'] != df['side'].shift()).cumsum())['side'].cumcount()

    return df['side'], df['memory']


def add_features(df: pd.DataFrame, features_dict):
    features = {
        feature: [
            [dict(config['config'], **{'kind': indicator_name}) for config in configs]
            for indicator_name, configs in indicator.items()]
        for feature, indicator in features_dict.items()}

    features_crossover = [feature for group in features['crossover'] for feature in group]
    ta_strategy = ta.Strategy(
        name="RMB",
        ta=features_crossover
    )

    df.ta.strategy(ta_strategy)

    add_features_dict = [dict(feature, **{'kind': indicator_name}) for indicator_name, features in
                         features_dict['crossover'].items() for feature in features]

    for feature in add_features_dict:
        # Build base and tholds names

        # rsi
        if feature['kind'] == 'rsi':
            feature['name'] = feature['base'] = 'RSI_{}'.format(feature['config']['length'])
        # bbands
        if feature['kind'] == 'bbands':
            feature['base'] = 'close'
            std = feature['config'].get('std', '2.0')
            feature['name'] = 'BB_{}_{}'.format(feature['config']['length'], std)
            feature['upper_thold'] = 'BBU_{}_{}'.format(feature['config']['length'], std)
            feature['down_thold'] = 'BBL_{}_{}'.format(feature['config']['length'], std)

        # Run crossover and append to df
        memory = feature['name'] + '_MEMO'
        side = feature['name'] + '_SIDE'

        if isinstance(feature['upper_thold'], int):
            upper_thold = pd.Series(feature['upper_thold'], index=np.arange(len(df)))
        elif isinstance(feature['upper_thold'], str):
            upper_thold = df[feature['upper_thold']]

        if isinstance(feature['down_thold'], int):
            down_thold = pd.Series(feature['down_thold'], index=np.arange(len(df)))
        elif isinstance(feature['down_thold'], str):
            down_thold = df[feature['down_thold']]

        df[memory], df[side] = crossover(base=df[feature['base']],
                                         upper_thold=upper_thold,
                                         upper_side=feature['upper_side'],
                                         down_thold=down_thold,
                                         down_side=feature['down_side']
                                         )

    return df


ohlc = pd.read_csv('./data/btc_1min.csv')
features_dict = {
    'crossover': {
        'rsi': [
            {'upper_thold': 70, 'upper_side': PositionSide.SHORT, 'down_thold': 30, 'down_side': PositionSide.LONG, 'config': {'length': 14}},
            {'upper_thold': 65, 'upper_side': PositionSide.SHORT, 'down_thold': 35, 'down_side': PositionSide.LONG, 'config': {'length': 21}},
            {'upper_thold': 60, 'upper_side': PositionSide.SHORT, 'down_thold': 40, 'down_side': PositionSide.LONG, 'config': {'length': 28}},
        ],
        'bbands': [
            {'upper_side': PositionSide.SHORT, 'down_side': PositionSide.LONG, 'config': {'length': 20}},
            {'upper_side': PositionSide.SHORT, 'down_side': PositionSide.LONG, 'config': {'length': 30, 'mamode': 't3'}},
        ]
    },
    'intersection': {
        'macd': [
            {'series1': 'MACD_{}_{}', 'series1_breakup_side': PositionSide.LONG, 'series2': 'MACDs_{}_{}', 'series2_breakup_side': PositionSide.SHORT, 'config': {'length': 30}}
        ]
    }
}

features_df = add_features(ohlc, features_dict)

a=1