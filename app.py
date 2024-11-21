import streamlit as st
import pandas as pd


#side bar width
# Add custom CSS to change sidebar width

#load master df
df_main=pd.read_csv('final_df.csv')

last_date=df_main['last_date'].values[0]
print(f'Debug: Last Date: {last_date}')
st.title(f'SNP500 Screener [{last_date}]')
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"] {
#         width: 100px; /* Adjust the width as needed */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


#cteate a stramlit 
side_bar_select_text=['sector_watch','snp_watch','individual_ticker'] #options 
sectors_list=pd.unique(df_main['sector']) #select a sector
features=['top_gainers','top_loser','all_time_high','all_time_low','week_up','month_up','year_up','']

print(f"Debug: {sectors_list}")

side_bar_selection=st.sidebar.selectbox('select an option',side_bar_select_text)

print(f'side_bar_selection: {side_bar_selection}') 

if side_bar_selection=='sector_watch':
    sector_selection=st.sidebar.selectbox('select a sector',sectors_list)
    print(f'Debug: sector selection; {sector_selection}')
    temp_df=df_main[df_main['sector']==sector_selection].reset_index(drop=True)
    #st.write(sector_df)

if side_bar_selection=='snp_watch':
    temp_df=df_main.copy()
    #st.write(df_main)
#st.write(temp_df.sort_values(by='ticker').reset_index(drop=True))

#function to display the dataframe based on the option chosen need to change later for %

def get_filtered_df(condition,ascending=True,df=temp_df):
    d=df.sort_values(by=condition,ascending=ascending).reset_index(drop=True)
    return d

gainer_loser_key_values={\
    'last_day':'last_change_pct',\
    'this_week':'pct_change_latest_week',
    'this_month':'pct_change_latest_month',
    'ytd':'pct_change_latest_year'
}
#add features
#features=['top_ten_gainers','top_ten_loser']

#page title 
if side_bar_selection in ['sector_watch','snp_watch']:
#gainer loser selection in side bar
    parameter_selection=st.sidebar.radio('Parameters:',['Gainer','Loser','SMA'])

    if parameter_selection in ['Gainer','Loser']:
        gainer_radio_option=st.sidebar.radio(
       'time_range',
        ('last_day','this_week','this_month','ytd'),)
        print(f'parameter-button: {parameter_selection} radio_option: {gainer_radio_option}')
        condition=gainer_loser_key_values[gainer_radio_option]
        ascending=True
        if parameter_selection=='Gainer':ascending=False
        con_df=get_filtered_df(condition=condition,ascending=ascending)

    if parameter_selection in ['SMA']:
        sma_radio_option=st.sidebar.radio(
            'sma_condition',
            (r'last_close > sma_50 & last_close > sma_200',r'last_close > sma_21',r'last_close > sma_50',r'last_close > sma_200')
        )
        print(f'parameter-button: {parameter_selection} radio_option: {sma_radio_option}')
        con_df=temp_df.query(sma_radio_option)


        #con_df=pd.DataFrame()
    st.write(con_df)

#show the df
#st.write(df_main.head())
