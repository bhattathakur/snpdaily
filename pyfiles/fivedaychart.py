#import libraries

import pandas as pd
#import numpy as np
from datetime import datetime,timedelta
from functools import reduce
import yfinance as yf
import matplotlib.pyplot as plt
#import seaborn as sns
import streamlit as st


def get_avawp(df,date):
  '''
  returns the anchored vwap in the form of list
  for given data frame based on closing price and volume
  begining with given date

  '''
  df=df[df['Date']>=date]
  price_cum_sum=(df['Close']*df['Volume']).cumsum() #cumsum of close*volume
  vol_cum_sum=df['Volume'].cumsum()                 #cumsum of vol
  #d='avwap'+date.replace('-','')
  d='avwap|'+date#.replace('-','')
  df[d]=(price_cum_sum/vol_cum_sum).round(2)

  return df[['Date',d]]

def get_merged_vwap(df):
  '''
  it returns a single dataframe with vwaps for given dates
  '''
  df=df.reset_index()
  all_df=[]

  unique_dates=list(df.Datetime.dt.date.unique())  #unique dates
  #print(f"unique-dates: {unique_dates}")

  for i in range(len(unique_dates)):
    temp_df=df[df['Datetime'].dt.date>=unique_dates[i]][['Ticker','Datetime','Close','Volume']]
    temp_df[f'avwap{i}']=(temp_df['Volume']*temp_df['Close']).cumsum()/temp_df['Volume'].cumsum()
    all_df.append(temp_df)
    #print(f'{i+1}')#\n{temp_df}')
    #display(temp_df)


  #merging the dataframes
  merged_dfs = reduce(lambda left,right: pd.merge(left, right, on=['Ticker','Datetime','Close','Volume'], how='left'), all_df).drop(columns=['Volume'])
  #display(merged_dfs.head(10))
  return merged_dfs.round(2)
  

def get_merged_vwap(df):
  '''
  it returns a single dataframe with vwaps for given dates
  '''
  df=df.reset_index()
  all_df=[]

  unique_dates=list(df.Datetime.dt.date.unique())  #unique dates
  #print(f"unique-dates: {unique_dates}")

  for i in range(len(unique_dates)):
    temp_df=df[df['Datetime'].dt.date>=unique_dates[i]][['Ticker','Datetime','Close','Volume']]
    temp_df[f'avwap{i}']=(temp_df['Volume']*temp_df['Close']).cumsum()/temp_df['Volume'].cumsum()
    all_df.append(temp_df)
    #print(f'{i+1}')#\n{temp_df}')
    #display(temp_df)


  #merging the dataframes
  merged_dfs = reduce(lambda left,right: pd.merge(left, right, on=['Ticker','Datetime','Close','Volume'], how='left'), all_df).drop(columns=['Volume'])
  #display(merged_dfs.head(10))
  return merged_dfs.round(2)

#single function for last 5 trading days
def get_single_vwap(ticker):
    '''
    This function is intended to get single vwap plot for last 5 trading days
    '''
    #download the data 
    data = yf.download(ticker, period='5d', interval="1m")

    debug=False
    if debug:print(f'head:\n {data.head().to_string()}')
    if debug:print(f'tail:\n {data.tail().to_string()}')

    if debug:print(f"Getting plot for: {ticker.upper()}")
    #temp_df=grouped.get_group(ticker).copy()
    temp_df=data.copy()
    temp_df['Ticker']=ticker
    merged_df=get_merged_vwap(temp_df)
    #display(temp_df.head())
    #display(merged_df.head())
    temp_plot=get_vwap_plot(merged_df)
    return temp_plot
  







