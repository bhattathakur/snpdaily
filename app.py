import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


#side bar width
# Add custom CSS to change sidebar width
st.set_page_config(layout="wide")  # Enable wide mode

#place_holder=st.empty()
#load master df
df_main=pd.read_csv('final_df.csv')

last_date=df_main['last_date'].values[0]
print(f'Debug: Last Date: {last_date}')
st.header(f'SNP500 Screener [{last_date}]')
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
side_bar_select_text=['snp_watch','sector_watch']#,'snp_watch']#,'individual_ticker'] #options 
hover_data=['ticker','security','last_close','last_change_pct','sma_21','sma_50','sma_200','pct_change_latest_week','pct_change_latest_month','pct_change_latest_year']
sectors_list=pd.unique(df_main['sector']) #select a sector
#features=['top_gainers','top_loser','all_time_high','all_time_low','week_up','month_up','year_up','']

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
        print(f'condition: {condition}')
        ascending=True
        if parameter_selection=='Gainer':ascending=False
        con_df=get_filtered_df(condition=condition,ascending=ascending)

        #looking for an alternative
        if parameter_selection=='Gainer':
            con_df=temp_df[temp_df[condition]>0].sort_values(by=condition,ascending=False)
        if parameter_selection=='Loser':
            con_df=temp_df[temp_df[condition]<0].sort_values(by=condition,ascending=True)

        plot_con_df=con_df.copy()

        #modify colors to bars
        colors=['lightgreen' if value>=0 else 'salmon' for value in plot_con_df[condition]]

        print(f"Debug: colors: {colors}")

        #title for gainer loser
        header_text=f'{parameter_selection.upper()}-{gainer_radio_option.upper()}'
        header_color='green' if 'GAINER' in header_text else 'red'
        #st.subheader(f'{parameter_selection.upper()}-{gainer_radio_option.upper()}')
        st.markdown(
    f"<h1 style='text-align: center;color:{header_color};'>{header_text}</h1>",
    unsafe_allow_html=True
)

        fig=px.bar(
            plot_con_df,x='ticker',y=condition,hover_data=hover_data,width=1600,height=800
        )
        fig.update_traces(marker_color=colors)


    if parameter_selection in ['SMA']:
        sma_radio_option=st.sidebar.radio(
            'sma_condition',
            (r'last_close > sma_50 & last_close > sma_200',\
             r'last_close > sma_21',r'last_close > sma_50',\
                r'last_close > sma_200',\
                 r'last_close-sma_21', r'last_close-sma_50',r'last_close-sma_200'\
                    )
        )
        print(f'parameter-button: {parameter_selection} radio_option: {sma_radio_option}')
        if sma_radio_option in [r'last_close-sma_21', r'last_close-sma_50',r'last_close-sma_200']:
            if sma_radio_option in [r'last_close-sma_21']:
                temp_df['last_close-sma_21']=temp_df['last_close']-temp_df['sma_21']
                st.subheader('DIFFERENCES BETWEEN LAST CLOSE AND SMA21')
                temp_df=temp_df.sort_values(by='last_close-sma_21')
                fig=px.bar(
                    temp_df,x='ticker',y='last_close-sma_21',hover_data=hover_data,width=1600,height=800
                )
                con_df=temp_df.copy()
            if sma_radio_option in [r'last_close-sma_50']:
                temp_df['last_close-sma_50']=temp_df['last_close']-temp_df['sma_50']
                st.subheader('DIFFERENCES BETWEEN LAST CLOSE AND SMA50')
                temp_df=temp_df.sort_values(by='last_close-sma_50')
                fig=px.bar(
                    temp_df,x='ticker',y='last_close-sma_50',hover_data=hover_data,width=1600,height=800
                )
                con_df=temp_df.copy()
            if sma_radio_option in [r'last_close-sma_200']:
                temp_df['last_close-sma_200']=temp_df['last_close']-temp_df['sma_200']
                st.subheader('DIFFERENCES BETWEEN LAST CLOSE AND SMA200')
                temp_df=temp_df.sort_values(by='last_close-sma_200')
                fig=px.bar(
                    temp_df,x='ticker',y='last_close-sma_200',hover_data=hover_data,width=1600,height=800
                )
                con_df=temp_df.copy()
        else:
            con_df=temp_df.query(sma_radio_option).sort_values(by='last_close').reset_index(drop=True)
            st.subheader(f'{sma_radio_option.upper()}')
            plot_con_df=con_df.copy()
            fig=px.bar(
             plot_con_df,x='ticker',y='last_close',hover_data=hover_data,width=1600,height=800
        )


        #con_df=pd.DataFrame()
    #st.write(con_df)

#con_df=con_df.head(10)

#fig=go.Figure(
#    data=[
#        go.Bar(x=con_df['ticker'],y=con_df['last_change_pct'],hover_data=hover_data)
#    ]
#)

# fig=px.bar(
#     con_df,x='ticker',y='last_change_pct',hover_data=hover_data,width=1600,height=800
# )
#fig.update_layout(hovermode='y unified')

st.plotly_chart(fig,use_container_width=True)
#show the df
#st.write(df_main.head())
