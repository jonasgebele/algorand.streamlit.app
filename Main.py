import streamlit as st
import pandas as pd

from datetime import time

import prices_utils as price_utils
import transactions_utils as transaction_utils
import chart
import sankey

def main():
    st.set_page_config(page_title='Algorand DEX Analytics', layout = 'wide', page_icon = './images/logo.jpg')

    #prices = pd.read_csv('./data/responses_28626240.csv')
    prices = pd.read_csv('./data/responses_27410001.csv')

    prices = price_utils.create_profit_deviation_boundaries(prices)
    prices = price_utils.create_dex_prices(prices)
    prices = price_utils.create_profitability_bool_per_dex(prices)
    prices = price_utils.get_ev_value_per_dex(prices)
    prices = price_utils.get_total_ev(prices)

    #transactions = pd.read_csv('./data/transactions_28626240.csv')
    transactions = pd.read_csv('./data/transactions_27410001.csv')
    transactions = transaction_utils.is_buy_or_sell_algo_swap(transactions)

    st.title("Algorand MEV Analytics") 
    data_expander = st.expander("Our dataframes")
    data_expander.caption("DEX Prices")
    data_expander.dataframe(prices)
    data_expander.caption("Transaction Data")
    data_expander.dataframe(transactions)



    st.header("ALGO DEX Prices")

    lowest_round = prices['round'].iloc[0].item()
    highest_round = prices['round'].iloc[-1].item()

    values = st.slider(
        "Rounds to display",
        value=(lowest_round, lowest_round+7500),
        min_value=lowest_round,
        max_value=highest_round
    )
    prices = prices[(prices['round'] >= values[0]) & (prices['round'] <= values[1])]
    fig =  chart.create_price_chart(prices)
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------------------------

    st.header("Theoretical Maximal Extractable Value (Potential DEX-CEX Arbitrage-Related MEV)")
    markets = [
            'TINYMAN(v2)_ALGO_USDC',
            'PACT_ALGO_USDC',
            'PACT_ALGO_USDT',
            'HUMBLESWAP_ALGO_USDC',
            'HUMBLESWAP_ALGO_USDT',
            'HUMBLESWAP_ALGO_goUSD',
            'ALGOFI_ALGO_USDT',
            'TINYMAN(v1.1)_ALGO_USDC',
            'TINYMAN(v1.1)_ALGO_USDT'
        ]
    market = st.selectbox('Market to be analyzed for theoretical Maximal Extractable Value', markets)
    fig = chart.extractable_value_chart(prices, market)
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------------------

    st.header("Swap-Volume (Number of Swaps)")
    granularity = st.slider('Number of Rounds in each bar', 1, 100, 30)
    swap_count_per_round = transaction_utils.create_swap_count_per_round(transactions)
    counts_per_round_range = transaction_utils.counts_per_round_range(swap_count_per_round, granularity)
    fig = chart.create_count_plot(counts_per_round_range)
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------------------------

    st.header("Dominant Market Participants Analysis")
    num_senders = st.slider('Number of biggest Senders (Descending)', 1, 27, 20)
    fig = sankey.create_sankey_graph(transactions, num_senders, 10)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
