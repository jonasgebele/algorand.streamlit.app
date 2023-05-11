import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def get_transaction_rounds_of(sender: str, df):
    sender_transaction_rounds = df.loc[df['sender'] == sender, 'round'].tolist()
    return sender_transaction_rounds

def get_color_list(n):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta', 'black', 'white', 'gray', 'pink', 'brown', 'olive', 'navy', 'teal']
    return colors[:n]

def create_price_chart(prices):
    y_columns = [
        'Binance_ALGOUSDT',
        'PACT_ALGO_USDC',
        'PACT_ALGO_USDT',
        'HUMBLESWAP_ALGO_USDC',
        'HUMBLESWAP_ALGO_USDT',
        'HUMBLESWAP_ALGO_goUSD',
        'ALGOFI_ALGO_USDC',
        'ALGOFI_ALGO_USDT',
        'TINYMAN(v1.1)_ALGO_USDC',
        'TINYMAN(v1.1)_ALGO_USDT',
        'TINYMAN(v2)_ALGO_USDC'
    ]
    
    default_hidden = [
        'PACT_ALGO_USDT',
        'HUMBLESWAP_ALGO_USDC',
        'HUMBLESWAP_ALGO_goUSD',
        'TINYMAN(v1.1)_ALGO_USDC',
        'TINYMAN(v1.1)_ALGO_USDT'
    ]

    fig = go.Figure()

    for column in y_columns:
        if column in default_hidden:
            fig.add_trace(
                go.Scatter(
                    x=prices['round'],
                    y=prices[column],
                    name=column,
                    visible="legendonly",  # make it hidden by default
                    line_shape='hv'
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=prices['round'],
                    y=prices[column],
                    name=column,
                    line_shape='hv'
                )
            )

    fig.add_scatter(
        x=prices['round'],
        y=prices['Binance_ALGOUSDT_UPD'],
        mode='lines',
        line=dict(width=0.5, color='black'),
        showlegend=False)
    fig.add_scatter(
        x=prices['round'],
        y=prices['Binance_ALGOUSDT_LPD'],
        mode='lines',
        line=dict(width=0.5, color='black'),
        showlegend=False)
    fig.update_layout(
        xaxis=dict(
            title="Block-Number (Round)",
            showgrid=False,
            gridwidth=0.05,
            dtick=200,
            tickformat='.0f'),
        yaxis=dict(
            title_text="ALGO Price"),
        legend=dict(
            yanchor="top",
            xanchor="left",
            orientation="h"
        )
    )

    return fig

def create_count_plot(df):
    fig = go.Figure(go.Bar(x=df['round'], y=df['count'], width=1))
    fig.update_layout(
        title='Round Counts',
        xaxis_title='Round',
        yaxis_title='Count'
    )
    return fig

def create_dual_axis_plot(counts, prices):
    counts['round'] = counts['round'].str.split('-').str[0]
    count_trace = go.Bar(x=counts['round'], y=counts['count'], name='Tx-Count')
    price_trace = go.Scatter(x=prices['round'], y=prices['total_ev'], name='Extractable Value', line=dict(color='red'))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(count_trace, secondary_y=False)
    fig.add_trace(price_trace, secondary_y=True)

    fig.update_layout(title='Round Counts and Price', xaxis_title='Round', xaxis_tickformat='d')
    fig.update_yaxes(title_text='Transaction Count', secondary_y=False)
    fig.update_yaxes(title_text='Extractable Value', secondary_y=True , type='log')
    return fig










def split_market_pair(s):
    split_str = s.split('_')
    market = split_str[0]
    pair = split_str[1]
    return market, pair

def extractable_value_chart(df, dex):
    market, pair = split_market_pair(dex)
    trace1 = go.Scatter(
        x=df['round'],
        y=df[dex],
        name=f'Price {pair} ({market})',
        yaxis='y'
    )
    trace2 = go.Scatter(
        x=df['round'],
        y=df[dex + "_ev"],
        name='Theoretically Maximal Extractable Value',
        yaxis='y2',
        line=dict(
            color='red'
        )
    )
    trace3 = go.Scatter(
        x=df['round'],
        y=df['Binance_ALGOUSDT_LPD'],
        yaxis='y',
        name='_nolegend_',
        showlegend=False,
        line=dict(
            color='black',
            width=0.5
        )
    )
    trace4 = go.Scatter(
        x=df['round'],
        y=df['Binance_ALGOUSDT_UPD'],
        yaxis='y',
        name='_nolegend_',
        showlegend=False,
        line=dict(
            color='black',
            width=0.5
        )
    )
    layout = go.Layout(
        title=f'{pair} price-chart on {market} with theoretically Maximal Extractable Value',
        xaxis=dict(
            tickformat='.0f',
            title='Block Number'
        ),
        yaxis=dict(
            title=f'{pair} price'
        ),
        yaxis2=dict(
            title='Theoretically Maximal Extractable Value ($)',
            overlaying='y',
            side='right',
            type='log'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)

def total_ev_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['round'],
        y=df['total_ev'],
        mode='lines',
        name='Total EV')
    )
    fig.update_layout(
        title='Total Theoretically Maximal Extractable Value across all analyzed pairs and DEX\'s',
        xaxis_title='Block Number',
        yaxis_title='Total Theoretically Maximal Extractable Value',
        yaxis_type='log',
        xaxis=dict(
            tickformat='.0f'
        ),
    )
    return fig

def total_dex_ev_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['round'],
        y=df['total_dex_ev'],
        mode='lines',
        name='Total EV')
    )
    fig.update_layout(
        title='Total extractable value across all DEX\'es on ALGO/USD',
        xaxis_title='Round1',
        yaxis_title='Total EV',
        yaxis_type='log',
        xaxis=dict(
            tickformat='.0f'
        ),
    )
    return fig
