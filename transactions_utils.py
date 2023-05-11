import pandas as pd

def is_buy_or_sell_algo_swap(df): # sell algo=1, buy algo=0
    for index, row in df.iterrows():
        if row['asset_id_send'] == 0 and row['asset_id_received'] == 0:
            df.drop(index, inplace=True)
        elif row['asset_id_send'] == 0 and row['asset_id_received'] != 0:
            df.at[index, 'buy_sell'] = 1
        elif row['asset_id_send'] != 0 and row['asset_id_received'] == 0:
            df.at[index, 'buy_sell'] = 0
        else:
            df.drop(index, inplace=True)
    return df

def create_swap_count_per_round(df, start_round=None, end_round=None):
    if start_round is None:
        start_round = df['round'].min()
    if end_round is None:
        end_round = df['round'].max()
    rounds = pd.Series(range(start_round, end_round + 1), name='round')
    swap_count_per_round = pd.merge(rounds, df.groupby('round').size().reset_index(name='count'), on='round', how='left')
    swap_count_per_round['count'] = swap_count_per_round['count'].fillna(0).astype(int)
    return swap_count_per_round

def counts_per_round_range(swap_count_per_round, round_range):
    if round_range > 1:
        num_ranges = swap_count_per_round.shape[0] // round_range
        counts_per_range = pd.DataFrame(columns=['round', 'count'])
        for i in range(num_ranges):
            start = i * round_range
            end = start + round_range - 1
            current_range = f"{swap_count_per_round['round'][start]}-{swap_count_per_round['round'][end]}"
            count_sum = swap_count_per_round['count'][start:end].sum()
            new_info = {'round': current_range, 'count': count_sum}
            counts_per_range = pd.concat([counts_per_range, pd.DataFrame([new_info])], ignore_index=True)
        return counts_per_range
    else:
        return swap_count_per_round