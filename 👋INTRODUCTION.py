import streamlit as st
import pandas as pd
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
st.snow()

# warning and disclaimer
last_date=pd.read_csv('df_combined.csv')['last_date'].iloc[0]
last_day_name=pd.to_datetime(last_date).strftime('%A')
disclaimer_text="""
Disclaimer:
The information provided by this stock screener is for informational purposes only and should not be considered as financial advice, investment advice, or trading suggestions. All data and analysis are provided "as is" and without any guarantees of accuracy or completeness. Users are solely responsible for their investment decisions. Always conduct your own research and consult with a licensed financial advisor before making any investment decisions.
"""
st.warning(disclaimer_text,icon="⚠️")
st.warning(f'RESULTS ARE BASED ON LAST-TRADING DAY: {last_date}, {last_day_name} ',icon="⚠️")


st.markdown(f"<h2 style='text-align:center;color:magenta;font-weight:bold;font-family:monospace;font-size:35px'>SIMPLE SCREENER, CHART & INFORMATION</h2>",unsafe_allow_html=True)
st.markdown("""
        <div class='custom-font'>
1. MARKET OVERVIEW gives broad insight of the market (like gainers, losers, etc) for different indices or sectors in different tabs.<br>
2. The SCREENER and corresponding tabs BAR_CHART, PIE_CHART, INFO_TABLE allows to view the top gainers and losers for various timeframes: the last trading day, last week, last month, and Year-to-Date (YTD).<br>
3. Corresponding "DOWNLOADABLE" table with all information is generated at "INFO-TABLE" for the selection at "SCREENER."<br>
4. You can filter tickers in the screener by indices such as the S&P 500, S&P 500 Sectors, NASDAQ 100, Dow 30 or IPO (YEAR>=2020), providing valuable insights for more granular market observation.<br>
5. The SMA-N-MISC indicator helps assess the position of the last price relative to key Simple Moving Averages (SMA) —5, 10, 21, 50, and 200 periods — which can indicate potential mean reversion opportunities. <br>
6. SMA-N-MISC also includes data on the 52-week highs and lows, enhancing trend analysis. <br>
7. The ATR% in SMA-N-MISC shows the Average True Range (ATR) relative to the closing price, which can be useful for both options and stock trading strategies.<br>
8. SMA-N-MISC ranks stocks based on their trading volume and Relative Strength Index (RSI), offering a quick snapshot of stock performance.<br>
8. The indicator tracks stocks that are making higher or lower closes over a 3-day period, highlighting potential short-term trends.<br>
10. The DAILY CHART feature generates a yearly chart for given index or ticker and provides ALL-TIME key information about the stock’s performance.
11. Pie chart is also helpful to visualize the parameter change over the time.<br>
12. This screener also features a 1 minute CandleStick Chart for last FIVE BUSINESS DAYS for any valid tickers or indices.<br>
13. Now, the screener also includes the information of stocks for IPO Year >=2020.
</div>

        """,unsafe_allow_html=True)
st.markdown("\ncontact: bhattathakur2015@gmail.com")
