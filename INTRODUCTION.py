import streamlit as st
st.set_page_config(layout='wide')

# Define custom CSS for styling text
custom_css = """
    <style>
        .custom-font {
            font-family: monospace;
            font-size: 25px;
            font-color:green;
        }
    </style>
"""

# Inject custom CSS into Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)



st.markdown(f"<h2 style='text-align:center;color:magenta;font-weight:bold;font-family:monospace;font-size:35px'>SIMPLE SCREENER, CHART & INFORMATION</h2>",unsafe_allow_html=True)
st.markdown("""
        <div class='custom-font'>
1. The screener allows you to view the top gainers and losers for various timeframes: the last trading day, last week, last month, and Year-to-Date (YTD).<br>
2. You can filter tickers in the screener by indices such as the S&P 500, S&P 500 Sectors, NASDAQ 100, or Dow 30, providing valuable insights for more granular market observation.<br>
3. The SMA-N-MISC indicator helps assess the position of the last price relative to key Simple Moving Averages (SMA) — 21, 50, and 200 periods — which can indicate potential mean reversion opportunities. <br>
4. SMA-N-MISC also includes data on the 52-week highs and lows, enhancing trend analysis. <br>
5. The ATR% in SMA-N-MISC shows the Average True Range (ATR) relative to the closing price, which can be useful for both options and stock trading strategies.<br>
6. SMA-N-MISC ranks stocks based on their trading volume and Relative Strength Index (RSI), offering a quick snapshot of stock performance.<br>
7. The indicator tracks stocks that are making higher or lower closes over a 3-day period, highlighting potential short-term trends.<br>
8. The CHART feature generates a yearly chart for each ticker and provides key information about the stock’s performance.
</div>
        """,unsafe_allow_html=True)
