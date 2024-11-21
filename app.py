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
side_bar_select_text=['individual_ticker','sector_watch','snp_watch'] #options 
sectors_list=pd.unique(df_main['sector']) #select a sector
features=['top_gainers','top_loser','all_time_high','all_time_low','week_up','month_up','year_up','']

print(f"Debug: {sectors_list}")

side_bar_selection=st.sidebar.selectbox('select an option',side_bar_select_text)

print(f'side_bar_selection: {side_bar_selection}') 

if side_bar_selection=='sector_watch':
    sector_selection=st.sidebar.selectbox('select a sector',sectors_list)
    print(f'Debug: sector selection; {sector_selection}')
    sector_df=df_main[df_main['sector']==sector_selection].reset_index(drop=True)
    st.write(sector_df)

if side_bar_selection=='snp_watch':
    st.write(df_main)


#page title 


#show the df
#st.write(df_main.head())
