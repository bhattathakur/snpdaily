
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import sys


st.set_page_config(layout='wide')
st.balloons()


#all_ticker_data_file

data_file='one_year_combined_df.csv'

temp_df=pd.read_csv(data_file)

#print(f"Debug: {temp_df.tail()}")

unique_tickers=pd.unique(temp_df['ticker'])

#print(f"Debug: unique_tickers {unique_tickers}")


ticker=st.sidebar.text_input("Enter a ticker from SNP500, NASDAQ100,IPO>=2020 or DOW30",value='NVDA').upper()
#ticker=ticker.upper()

if ticker not in unique_tickers:
    st.warning(f'{ticker} is not in SNP500, NASDAQ100 or DOW30',icon="⚠️")
    sys.exit(1)
else:
    df=temp_df[temp_df['ticker']==ticker].sort_values(by=['Date']).reset_index(drop=True)
    last_date=df['Date'].iloc[-1].split()[0]#.values[0]
    df['SMA_5'] = df['Close'].rolling(5).mean()
    df['SMA_10'] = df['Close'].rolling(10).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()
    df['SMA_200'] = df['Close'].rolling(200).mean()
    #smas for legend
    sma5=df['SMA_5'].iloc[-1]
    sma10=df['SMA_10'].iloc[-1]
    sma50=df['SMA_50'].iloc[-1]
    sma200=df['SMA_200'].iloc[-1]
    # Calculate VWAP
    df['Price * Volume'] = df['Close'] * df['Volume']
    df['Cumulative Price * Volume'] = df['Price * Volume'].cumsum()
    df['Cumulative Volume'] = df['Volume'].cumsum()
    df['VWAP'] = df['Cumulative Price * Volume'] / df['Cumulative Volume']
    vwap=df['VWAP'].iloc[-1]
    close=df['Close'].iloc[-1]

    # Drop intermediate columns if not needed
    df.drop(['Price * Volume', 'Cumulative Price * Volume', 'Cumulative Volume'], axis=1, inplace=True)
    df=df.round(2)
    #st.write(df)
#get the dataframe related to input ticker
data=[go.Candlestick(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],name=f'{ticker}-Candlestick [{close}]')]
#data=[go.Ohlc(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],name=f'{ticker}-Candlestick')]
sma5_data=go.Scatter(x=df['Date'],y=df['SMA_5'],mode='lines',name=f'SMA5 [{sma5:0.2f}]',line=dict(color='blue',width=2))
sma10_data=go.Scatter(x=df['Date'],y=df['SMA_10'],mode='lines',name=f'SMA10 [{sma10:0.2f}]',line=dict(color='green',width=2))
sma50_data=go.Scatter(x=df['Date'],y=df['SMA_50'],mode='lines',name=f'SMA50 [{sma50:0.2f}]',line=dict(color='yellow',width=2))
sma200_data=go.Scatter(x=df['Date'],y=df['SMA_200'],mode='lines',name=f'SMA200 [{sma200:0.2f}]',line=dict(color='red',width=2))
vwap_data=go.Scatter(x=df['Date'],y=df['VWAP'],mode='lines',name=f'VWAP [{vwap:0.2f}]',line=dict(color='orange',width=2))
#container 1
st.markdown(f"<h3 style='text-align:center;color:red'>ONE YEAR CHART & ALl INFOS FOR {ticker} </h3>",unsafe_allow_html=True)
with st.container():
    fig=go.Figure(data=data)
    fig.add_trace(sma5_data)
    fig.add_trace(sma10_data)
    fig.add_trace(sma50_data)
    fig.add_trace(sma200_data)
    fig.add_trace(vwap_data)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(
    width=1000,
    height=600,
    xaxis_title="Date",
    yaxis_title="Price ($)",)

    fig.update_xaxes(
            rangebreaks=[
                dict(bounds=['sat','mon']) #hide weekends
                ]
            )

    #show chart
    st.plotly_chart(fig,use_container_width=True)
#update

#read the information file
df_info=pd.read_csv('df_combined.csv').query('ticker==@ticker')
#print(df_info)
#Convert the single row into a nicely formatted string
row_dict = df_info.iloc[0].to_dict()  # Convert the row to a dictionary

# Use markdown or text for better display
formatted_text = "\n".join([f"**{key}:** {value}" for key, value in row_dict.items()])

# Display it in Streamlit
#container1=st.container(boarder=True)
with st.container():
    st.markdown(f"<h3 style='text-align:center',>✨ INFO TABLE ✨</h3>",unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    # Display items in each column
    for idx, (key, value) in enumerate(row_dict.items()):
        if idx % 3 == 0:  # First column
            col1.markdown(f"<p style='color:orchid;font-size:20px;font-weight:bold;font-family:monospace'>{key:.<24}: {value}</p>",unsafe_allow_html=True)
        elif idx % 3 == 1:  # Second column
            col2.markdown(f"<p style='color:lightgreen;font-size:20px;font-weight:bold;font-family:monospace'>{key:.<24}: {value}</p>",unsafe_allow_html=True)
            #col2.markdown(f"**{key}:** {value}")
        else:  # Third column
            #col3.markdown(f"**{key}:** {value}")
            col3.markdown(f"<p style='color:salmon;font-size:20px;font-weight:bold;font-family:monospace'>{key:.<24}: {value}</p>",unsafe_allow_html=True)
#st.markdown("### User Details")
st.markdown("\ncontact info: bhattathakur2015@gmail.com")
#st.markdown(formatted_text)
#last_date=st.session_state.get('last_date')
st.sidebar.info(f"RESULTS BASED ON {last_date}",icon="ℹ️")

