import streamlit as st
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import prices_utils as price_utils

import sankey
import network
import chart

def test():
    '''
    TRANSACTION_FILE = f'./data/transactions_27410001.csv'
    transactions = pd.read_csv(TRANSACTION_FILE)
    transactions = delete_outside_transactions(transactions)
    print(transactions)
    fig = chart.extractable_value_chart(prices, 'HUMBLESWAP_ALGOgoUSD')
    st.plotly_chart(fig, use_container_width=True)

    #min_round, max_round = get_max_min_rounds(transactions)
    #start_round, end_round = st.select_slider(
    #    'Select a rounds you want to display',
    #    options=transactions[['round']],
    #    value=(min_round, max_round))
    #transactions = get_rounds_between(transactions, start_round, end_round)

    biggest_senders_list = get_n_biggest_senders(transactions, 10)

    chart_fig = chart.create_price_chart(prices, transactions, biggest_senders_list)
    st.plotly_chart(chart_fig, use_container_width=True)

    sankey_fig = sankey.create_sankey_graph(transactions, 100)
    st.plotly_chart(sankey_fig, use_container_width=True)

    network_fig = network.create_network_graph(transactions)
    st.plotly_chart(network_fig, use_container_width=True)

    #volume_fig = volume.plot_volume_trades(transactions)
    #st.plotly_chart(volume_fig, use_container_width=True)

    st.json(transactions.to_dict(), expanded=False)
    '''
    pass

def delete_outside_transactions(transactions):
    markets = pd.read_csv("./data/markets.csv")
    market_addresses = markets['address'].tolist()
    transactions = transactions[transactions['receiver'].isin(market_addresses)]
    return transactions

def get_n_biggest_senders(df_txs, n):
    sender_counts = df_txs.groupby('sender')['sender'].count().sort_values(ascending=False)
    return sender_counts[:n]

def get_max_min_rounds(df):
    max_round = df['round'].max()
    min_round = df['round'].min()
    return min_round, max_round

def get_rounds_between(df, start_round, end_round):
    return df.loc[(df['round'] >= start_round) & (df['round'] <= end_round)]

def main():
    st.set_page_config(page_title='Algorand DEX Analytics', layout = 'wide', page_icon = './images/logo.jpg')
    st.title("Algorand DEX Analytics")

    PRICE_HISTORY_FILE = f'./../data/responses_28626240.csv'    
    prices = pd.read_csv(PRICE_HISTORY_FILE)

    prices = price_utils.create_profit_deviation_boundaries(prices)
    prices = price_utils.create_dex_prices(prices)
    prices = price_utils.create_profitability_bool_per_dex(prices)
    prices = price_utils.get_ev_value_per_dex(prices)

    fig =  chart.create_price_chart(prices)
    st.plotly_chart(fig, use_container_width=True)
    
if __name__ == "__main__":
    main()
