import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time as t
import datetime
import pytz
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#import pandas_ta as ta
#import talib

st.set_page_config(layout='wide') #wide page


est_timezone=pytz.timezone('US/Eastern')

#sidebar with datetime (updating) and options for ticker choice including BTC-USD And ETH-USD
debug=False

current_date_time=datetime.datetime.now(est_timezone)#
current_date=current_date_time.date()

#last 5 bussiness days
#last_bussiness_days=pd.bdate_range(end=current_date,periods=5)#[0]
#st.write(f'last_bussiness_days:{last_bussiness_days}')

mag7=['AAPL','NVDA','TSLA','META','AMZN','GOOGL','MSFT','MSTR','AMD','GME','DJT','SMCI']
indices=['^GSPC','^IXIC','^DJI','^RUT']
current_time_text=f"{current_date_time.strftime('%A, %I:%M %p, %Y-%m-%d')}"

#check_date_time=True
plot_placeholder=st.empty() #VERY important for refreshing the same plot otherwise each plot will append

#user has two options input their own ticker or choose from the options
choose_radio_options=['CHOOSE FROM LIST','INPUT YOUR TICKER']# if check_date_time else ['CHOOSE FROM LIST']
radio_value=st.sidebar.radio("INPUT METHOD",choose_radio_options,key='input_method')

#user_value=st.sidebar.selectbox("SELECT or INPUT YOUR TICKER",indices+mag7,index=0,key='user_choice')

if radio_value==choose_radio_options[0]:
    user_value=st.sidebar.selectbox("SELECT",indices+mag7,key='mag7',index=0)
else:
    user_value=st.sidebar.text_input("INPUT YOUR TICKER",key='user_input').upper()


st.sidebar.markdown(f'CHOSEN TICKER: {user_value}')

#ticker
#get informative df
def get_informative_df(df):
  temp_df=df.copy()
  temp_df['sma5']=get_sma(temp_df,'Close',5)
  temp_df['sma10']=get_sma(temp_df,'Close',10)
  temp_df['vol5']=get_sma(temp_df,'Volume',5)
  #temp_df['vol10']=get_sma(temp_df,'Volume',10)
  temp_df['typical_price']=(temp_df['High']+temp_df['Low']+temp_df['Close'])/3
  temp_df['vwap']=(temp_df['Volume']*temp_df['typical_price']).cumsum()/temp_df['Volume'].cumsum()
  temp_df['rsi']=calculate_rsi(temp_df['Close'])
  temp_df['TR1']=temp_df['High']-temp_df['Low']
  temp_df['TR2']=(temp_df['High']-temp_df['Close'].shift(1)).abs()
  temp_df['TR3']=(temp_df['Low']-temp_df['Close'].shift(1)).abs()
  temp_df['tr']=temp_df[['TR1','TR2','TR3']].max(axis=1)
  temp_df['atr5']=temp_df['tr'].rolling(window=5).mean()

  #dropping_columns
  dropping_cols=['TR1','TR2','TR3','typical_price']
  temp_df=temp_df.drop(dropping_cols,axis=1)
  return temp_df.round(2)
ticker=user_value #will be used in a plot
try:
    temp_df=yf.download(ticker,period='max',interval='1m',group_by='tickers')
    # Check if DataFrame is empty
    if temp_df.empty:
        st.warning('Error Occured, Enter a correct ticker or try again later !',icon="⚠️")
        st.stop()
except:
    st.warning('Error Occured, Enter a correct ticker or try again later !',icon="⚠️")
    st.stop()

#this is needed if using the online services like google colab
#debug=True
if debug:st.write(temp_df)
temp_df=temp_df[ticker]#.reset_index(drop=False) #on remote deployment

temp_df=temp_df.reset_index(drop=False) #reset_index

if debug:st.write(temp_df)

#get unique dates from the 1m dataframe
temp_df['Datetime']=pd.to_datetime(temp_df['Datetime'])
temp_df['Datetime']=temp_df['Datetime'].dt.tz_convert(est_timezone)

if debug:st.write(temp_df)

#grouped_df=df.groupby(pd.to_datetime(df['Datetime']).dt.date)
last_bussiness_days=pd.unique(temp_df['Datetime'].dt.date)
if debug:st.write(f"last_bussiness_days: {last_bussiness_days}")

date_chosen=st.sidebar.radio("CHOOSE AVAILABLE DATES",sorted(last_bussiness_days,reverse=True)+['last_5business_days'],index=0)
st.sidebar.write(f'CHOSEN DATE: {date_chosen}')

#get df based on chosen date
df=temp_df.copy() if date_chosen=='last_5business_days' else temp_df[temp_df['Datetime'].dt.date==date_chosen]
if debug:st.write(df)


#if debug:st.stop()
#user defined functions
def get_sma(df,parameter,period):
  'smas for close or volume '
  return df[parameter].rolling(period).mean()

def calculate_rsi(close_prices, timeperiod=14):
    """
    Calculate the Relative Strength Index (RSI) for a given series of close prices using pandas.
    
    Parameters:
    - close_prices (list or pd.Series): The closing prices for which to calculate the RSI.
    - timeperiod (int, optional): The period to use for calculating the RSI. Default is 14.
    
    Returns:
    - pd.Series: The RSI values.
    """
    # Convert the input to a pandas Series if it's not already
    close_prices = pd.Series(close_prices)
    
    # Calculate the daily price changes
    delta = close_prices.diff()
    
    # Separate the gains and losses
    gain = delta.where(delta > 0, 0)  # Gain is the positive change
    loss = -delta.where(delta < 0, 0)  # Loss is the negative change (as positive values)
    
    # Calculate the rolling average of gains and losses over the specified period
    avg_gain = gain.rolling(window=timeperiod, min_periods=1).mean()
    avg_loss = loss.rolling(window=timeperiod, min_periods=1).mean()
    
    # Calculate the relative strength (RS)
    rs = avg_gain / avg_loss
    
    # Calculate the RSI using the formula RSI = 100 - (100 / (1 + RS))
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

#define a function for text to audio
def text_to_audio(text,ticker=ticker):
    js_code = f"""
    <script>
        const msg = new SpeechSynthesisUtterance("{ticker} {text}");
        msg.lang = 'en-US';  // Set the language (customize as needed)
        msg.pitch=0.8;
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0,width=0)




want_minute_data=True
if(want_minute_data):
    # if(debug):st.write(df.tail())
    # if(debug):st.write(f"df columns: {df.columns}")
    # on_local=False
    # if not on_local:df=df[ticker].reset_index(drop=False) #This is turned on the app deployment and turned off in local
    # df=df.reset_index(drop=False)
    # df['Datetime']=pd.to_datetime(df['Datetime']) #Needed for a local
    # #df.loc[:,ticker]=ticker
    # debug=True
    if(debug):st.write(f"df columns: {df.columns}")
    df['Volume']=df['Volume'].div(1e6)
    df['Datetime']=df['Datetime'].dt.tz_convert(est_timezone)#.dt.strftime('%Y-%m-%d %H:%M')
    info_df=get_informative_df(df)
    if(debug):st.write(f"info_df columns: {info_df.columns}")
    #last row
    last_row=info_df.iloc[-1]
    #open,low,high,total_volume
    open=round(df['Open'].iloc[0],2)
    low=round(df['Low'].min(),2)
    high=round(df['High'].max(),2)
    existing_date=last_row.at['Datetime'].date()
    total_volume=round(df['Volume'].sum(),2)
    if debug:st.write(f"open: {open}")
    if debug:st.write(f"Low: {low}")
    if debug:st.write(f"High: {high}")
    if debug:st.write(f"Volume: {total_volume}")
    if debug:st.write(f"existing_date: {existing_date}")

    close=last_row.at['Close']
    #change=last_row.at['change']
    #pct_change=last_row.at['pct_change']
    volume=last_row.at['Volume']
    volume5=last_row.at['vol5']
    #volume10=last_row.at['vol10']
    vwap=last_row.at['vwap']
    rsi=last_row.at['rsi']
    tr=last_row.at['tr']
    atr5=last_row.at['atr5']

    if(debug):st.write(f"last_row: {last_row}")
    if(debug):st.write(f"close: {close}")
    #if(debug):st.write(f"change: {change}")
    if(debug):st.write(f"pct_change: {pct_change}")
    if(debug):st.write(f"Volume: {volume}")
    if(debug):st.write(f"Volume5: {volume5}")
    if(debug):st.write(f"vwap: {vwap}")
    if(debug):st.write(f"rsi: {rsi}")
    if(debug):st.write(f"tr:{tr}")
    if(debug):st.write(f"atr5:{atr5}")
    if(debug):st.write(f"price_above_vwap:{price_above_vwap}")
    if(debug):st.write(f"price_below_vwap:{price_below_vwap}")
    if(debug):st.write(f"sma5_gt_sma10:{sma5_gt_sma10}")
    if(debug):st.write(f"sma5_lt_sma10:{sma5_lt_sma10}")
    if(debug):st.write(f"higher_close:{higher_close}")
    if(debug):st.write(f"lower_close:{lower_close}")

    with plot_placeholder.container():
        st.markdown(f"<h4 Style='text-align:center;'>ONE DAY DATA FOR {user_value} </h4>",unsafe_allow_html=True)
        #row 1
        with st.container():
            col1,col2,col3,col4,col5,col6,col7=st.columns(7)
            with col1:
                st.metric(f"DATE:",str(existing_date))
            with col2:
                st.metric(f'TICKER',ticker)
            with col3:
                st.metric(f'OPEN',open)
            with col4:
                st.metric(f'LOW',low)
            with col5:
                st.metric(f'HIGH',high)
            with col6:
                st.metric(f'CLOSE',close)
            with col7:
                st.metric('VOLUME (M)',total_volume)

        fig=make_subplots(rows=3,cols=1,shared_xaxes=False,vertical_spacing=0.05,row_heights=[0.6,0.2,0.2])

        #first row
        fig.add_trace(go.Candlestick(x=info_df['Datetime'],open=info_df['Open'], high=info_df['High'],low=info_df['Low'],\
                close=info_df['Close'],name=f'{ticker}-Candlestick'),row=1,col=1)

        fig.add_trace(go.Scatter(x=info_df['Datetime'],y=info_df['sma5'],mode='lines',name='SMA5',line=dict(color='red')),row=1,col=1)
        fig.add_trace(go.Scatter(x=info_df['Datetime'],y=info_df['sma10'],mode='lines',name='SMA10',line=dict(color='blue')),row=1,col=1)
        fig.add_trace(go.Scatter(x=info_df['Datetime'],y=info_df['vwap'],mode='lines',name='vwap',line=dict(color='orange')),row=1,col=1)

        #Define the times for vertical lines (using the existing date)
        times = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
        for time_str in times:
            time = pd.to_datetime(f"{existing_date} {time_str}")  # Combine date and time
            #print(f'time: {time}')
            fig.add_vline(x=time, line=dict(color='brown', width=0.5, dash='dot'),row=1,col=1)

        #second row
        fig.add_trace(go.Bar(x=info_df['Datetime'], y=info_df['Volume'], text=info_df['Volume'],textposition='auto',name='Volume', marker_color='grey'), row=2, col=1)
        fig.add_trace(go.Scatter(x=info_df['Datetime'],y=info_df['vol5'],mode='lines',name='volume5',line=dict(color='skyblue')),row=2,col=1)

        #third row
        fig.add_trace(go.Bar(x=info_df['Datetime'], y=info_df['tr'], text=info_df['tr'],textposition='auto',name='TR', marker_color='magenta'), row=3, col=1)
        fig.add_trace(go.Scatter(x=info_df['Datetime'],y=info_df['atr5'],mode='lines',name='ATR5',line=dict(color='lightgreen')),row=3,col=1)

        #horizontal line in x_min and x_max
        #date min and max for creating a horizontal line
        date_min=info_df['Datetime'].min()
        date_max=info_df['Datetime'].max()
        max_price=info_df['High'].max()
        min_price=info_df['Low'].min()

        #add the horizontal line at min and max value
        fig.add_shape(type='line',x0=date_min,y0=max_price,x1=date_max,y1=max_price,line=dict(color='lightgreen',width=1,dash='dash'),row=1,col=1)
        fig.add_shape(type='line',x0=date_min,y0=min_price,x1=date_max,y1=min_price,line=dict(color='salmon',width=1,dash='dash'),row=1,col=1)
        
        #generate custom tickers
        start_time=info_df['Datetime'].iloc[0].floor('5min')
        end_time=info_df['Datetime'].iloc[-1].floor('5min')
        custom_ticks_vals=pd.date_range(start=start_time,end=end_time,freq='5min')
        custom_ticks_text=[x.strftime('%H:%M') for x in custom_ticks_vals]
        #printtick labels
        #st.write(f'custom_ticks_vals: {custom_ticks_vals}')
        #st.write(f'custom_ticks_text: {custom_ticks_text}')

#        fig.update_layout(xaxis_rangeslider_visible=False,
#                xaxis=dict(tickmode='array',tickvals=custom_ticks_vals,ticktext=custom_ticks_text),
#                xaxis_tickformat='%H:%M',
#                width=1200,height=770,
#                )
#        fig.update_xaxes(
#                #xaxis=dict(tickmode='array',tickvals=custom_ticks_vals,ticktext=custom_ticks_text),
#                tickmode='array',tickvals=custom_ticks_vals,ticktext=custom_ticks_text,
#                xaxis_tickformat='%H:%M',
#                )
        fig.update_xaxes(
        tickmode='array',
        tickvals=custom_ticks_vals,
        ticktext=custom_ticks_text,
        tickformat='%H:%M',
        rangeslider_visible=False
        )
        fig.update_layout(
        width=1200,
        height=770
        )


        st.plotly_chart(fig,use_container_width=True)

