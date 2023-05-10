import streamlit as st
import pandas as pd

import prices_utils as price_utils
import chart

def main():
    st.set_page_config(page_title='Algorand DEX Analytics', layout = 'wide', page_icon = './images/logo.jpg')

    prices = pd.read_csv('./data/responses_28626240.csv')
    transactions = pd.read_csv('./data/transactions_28626240.csv')

    prices = price_utils.create_profit_deviation_boundaries(prices)
    prices = price_utils.create_dex_prices(prices)
    prices = price_utils.create_profitability_bool_per_dex(prices)
    prices = price_utils.get_ev_value_per_dex(prices)
    prices = price_utils.get_total_ev(prices)

    st.title("Algorand DEX Analytics") 
    st.header("Theoretical Extractable Value Dashboard")
    fig =  chart.create_price_chart(prices)
    st.plotly_chart(fig, use_container_width=True)
    data_expander = st.expander("Our scraped data")
    data_expander.dataframe(prices)

    st.header("Dominant Market Participants Analysis")
    st.write("Test")
    
if __name__ == "__main__":
    main()
