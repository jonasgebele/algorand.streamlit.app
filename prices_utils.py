import amm_price_calculations as amm_calc

import re
import pandas as pd

def convert_timestamp_column(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def get_dex_markets(df):
    all_columns = df.columns
    dex_markets = [col for col in all_columns if re.match(r'[A-Za-z\(\.\)\d]+_[A-Z]+_[A-Za-z]+', col)]
    markets = set([market.rsplit('_', 1)[0] for market in dex_markets])
    return [item for item in markets if item.count('_') == 2]

def extract_pairs_from_dex_name(dex):
    asset = '_'
    elements = dex.split(asset)
    return elements

def create_profit_deviation_boundaries(df):
    df['Binance_ALGOUSDT_LPD'] = df['Binance_ALGOUSDT'].apply(amm_calc.lower_profit_deviation)
    df['Binance_ALGOUSDT_UPD'] = df['Binance_ALGOUSDT'].apply(amm_calc.upper_profit_deviation)
    return df

def create_dex_prices(df):
    dexes = get_dex_markets(df)
    for dex in dexes:
        dex_info_list = extract_pairs_from_dex_name(dex)
        asset0_column = dex + "_[" + dex_info_list[1] + "]"
        asset1_column = dex + "_[" + dex_info_list[2] + "]"
        df[dex] = df[asset1_column] / df[asset0_column]
    return df

def create_profitability_bool_per_dex(df):
    dexes = get_dex_markets(df)
    for dex in dexes:
        df[dex + '_ldb'] = df[dex] < df['Binance_ALGOUSDT_LPD']
        df[dex + '_hdb'] = df[dex] > df['Binance_ALGOUSDT_UPD']
    return df

def calculate_extractable_value(row, dex):
    elements = extract_pairs_from_dex_name(dex)
    p = row['Binance_ALGOUSDT']
    X = row[dex + '_[' + elements[1] + "]"]
    Y = row[dex + '_[' + elements[2] + "]"]
    if X < Y:
        temp = X
        X = Y
        Y = temp
    ev = amm_calc.extractable_value_in_USD(p, X, Y)
    return ev

def get_ev_value_per_dex(df):
    dexes = get_dex_markets(df)
    for dex in dexes:
        df[dex + '_ev'] = df.apply(calculate_extractable_value, dex=dex, axis=1).apply('{:.2f}'.format)
    return df

def get_total_ev(df):
    dexes = get_dex_markets(df)
    df['total_ev'] = df.apply(lambda row: sum(max(0, float(row[dex + "_ev"])) for dex in dexes), axis=1)
    return df