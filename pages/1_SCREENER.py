import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")  # Enable wide mode
#data files sources
files_list={
'SNP500':'df_snp500.csv',
'SNP500-SECTOR':'df_snp500.csv',
'NASDAQ100':'df_nasdaq100.csv',
'DOW':'df_dow.csv',
}
side_bar_selection=st.sidebar.selectbox('select an option',files_list.keys())

print(f'Debug:side_bar_selection: {side_bar_selection}') 


#load master df
data_file=files_list[side_bar_selection]
print(f'Debug: data_file: {data_file}')
df_main=pd.read_csv(data_file) #read a file

#change up_3_days and down_3_days into bool
df_main['up_3_days']=df_main['up_3_days'].astype(bool)
df_main['down_3_days']=df_main['down_3_days'].astype(bool)

#print head of a file
#st.write(df_main.head(5))
#check 52 two week high and low
df_main['fiftytwoweek_low']=(df_main['last_close']==df_main['fiftytwo_week_low'])
df_main['fiftytwoweek_high']=(df_main['last_close']==df_main['fiftytwo_week_high'])

last_date=df_main['last_date'].values[0]
print(f'Debug: Last Date: {last_date}')
#st.header(f'SNP500 OVERVIEW [{last_date}]')
st.markdown(
f"<h4 style='text-align:center'> {side_bar_selection} OVERVIEW [{last_date}]</h4>",
unsafe_allow_html=True
)

#cteate a stramlit 
hover_data=['ticker','last_close','last_change_pct','sma_21','sma_50','sma_200',\
            'fiftytwo_week_high','fiftytwo_week_low','pct_change_latest_week','pct_change_latest_month','pct_change_latest_year']

if side_bar_selection=='SNP500-SECTOR':
    sectors_list=pd.unique(df_main['sector']) #select a sector
    print(f"Debug: {sectors_list}")
    sector_selection=st.sidebar.selectbox('select a sector',sectors_list)
    print(f'Debug: sector selection; {sector_selection}')
    st.markdown(
        f"<h5 style='text-align:center;color:darkorchid;'>{sector_selection}</h5>",
        unsafe_allow_html=True
    )
    temp_df=df_main[df_main['sector']==sector_selection].reset_index(drop=True)
    #st.write(sector_df)

if side_bar_selection in ['SNP500','NASDAQ100','DOW']:
    temp_df=df_main.copy()


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

#st.sidebar.text('contact: bhattathakur2015@gmail.com')
if side_bar_selection in ['SNP500','SNP500-SECTOR','DOW','NASDAQ100']:
#gainer loser selection in side bar
    parameter_selection=st.sidebar.radio('Parameters:',['Gainer','Loser','SMA-N-MISC'])

    if parameter_selection in ['Gainer','Loser']:
        gainer_radio_option=st.sidebar.radio(
       'time_range:',
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

        #print(f"Debug: colors: {colors}")

        #title for gainer loser
        header_text=f'{side_bar_selection}-{parameter_selection.upper()}-{gainer_radio_option.upper()}'
        header_color='green' if 'GAINER' in header_text else 'red'
        #st.subheader(f'{parameter_selection.upper()}-{gainer_radio_option.upper()}')
        st.markdown(
    f"<h2 style='text-align: center;color:{header_color};'>{header_text}</h2>",
    unsafe_allow_html=True
)

        fig=px.bar(
            plot_con_df,x='ticker',y=condition,hover_data=hover_data,width=1600,height=800
        )
        fig.update_traces(marker_color=colors)


    if parameter_selection in ['SMA-N-MISC']:
        apply_conditions=[
            r'last_close > sma_50 & last_close > sma_200',\
            r'last_close < sma_50 & last_close < sma_200',\
            r'fiftytwoweek_high',r'fiftytwoweek_low',\
            f'up_3_days',\
            f'down_3_days'
        ]
        other_conditions=[
            #r'fiftytwo_week_high',r'fiftytwo_week_low',\
            r'highest_volume',\
            r'highest_atr%',\
            r'highest_rsi',\
            r'last_close-sma_21', r'last_close-sma_50',r'last_close-sma_200',\
        ]
        radio_option_list=apply_conditions+other_conditions
        sma_radio_option=st.sidebar.radio(
            'Features:',
            radio_option_list
        )
        print(f'parameter-button: {parameter_selection} radio_option: {sma_radio_option}')

        #checking if the option is inside the sma_radio_option
        if sma_radio_option in apply_conditions:
            print(f'Debug: inside apply_condition')
            con_df=temp_df.query(sma_radio_option).sort_values(by='last_close').reset_index(drop=True)
            #st.subheader(f'{sma_radio_option.upper()}')

            #NOTE: using the index position to give the color of the bar plots
            index_of_radio_option=apply_conditions.index(sma_radio_option)
            print(f'Debug: index_of_radio_option: {index_of_radio_option}')
            h2_color='SlateBlue' #'red' if 'down' or 'low' in sma_radio_option else 'lightgreen'
            marker_color='red' if index_of_radio_option%2==1  else 'lightgreen'
            st.markdown(
                f"<h2 style='text-align:center;color:{h2_color};background-color:rgb(255, 230, 179,0.25);padding:3px'>{sma_radio_option.upper()}</h2>",
                unsafe_allow_html=True
                        )
            plot_con_df=con_df.copy()
            fig=px.bar(
             plot_con_df,x='ticker',y='last_close',hover_data=hover_data,width=1600,height=800
            )
            fig.update_traces(marker_color=marker_color)

        else:# sma_radio_option in [r'last_close-sma_21', r'last_close-sma_50',r'last_close-sma_200',r'up_three_days']:
            if sma_radio_option in [r'highest_volume']:
                par='last_volume(M)'
                st.markdown(f"<h3 style='text-align:center;color:OliveDrab'>HIGHEST {par.upper()}</h3>",unsafe_allow_html=True)
                temp_df=temp_df.sort_values(by=par,ascending=False)
                fig=px.bar(temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800)
                con_df=temp_df.copy()
            elif sma_radio_option in [r'highest_atr%']:
                par='atr%'
                st.markdown(f"<h3 style='text-align:center;color:OliveDrab'>HIGHEST {par.upper()} [ATR w.r.t. CLOSE]</h3>",unsafe_allow_html=True)
                temp_df=temp_df.sort_values(by=par,ascending=False)
                fig=px.bar(temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800)
                con_df=temp_df.copy()
            elif sma_radio_option in [r'highest_rsi']:
                par='rsi'
                st.markdown(f"<h3 style='text-align:center;color:OliveDrab'>HIGHEST {par.upper()} ",unsafe_allow_html=True)
                temp_df=temp_df.sort_values(by=par,ascending=False)
                fig=px.bar(temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800)
                con_df=temp_df.copy()

            elif sma_radio_option in [r'last_close-sma_21',r'last_close-sma_50',r'last_close-sma_200']:
                par=sma_radio_option
                sma_part=par.split('-')[1]
                last_close_part=par.split('-')[0]
                print(f"Debug: sma_radio_option: {par}\n sma_part: {sma_part}")
                temp_df[par]=temp_df['last_close']-temp_df[sma_part]
                #temp_df['last_close-sma_21']=temp_df['last_close']-temp_df['sma_21']
                st.markdown(
                    f"<h2 style='text-align:center;color:magenta'>{par.upper()}</h2>",unsafe_allow_html=True
                )
                #st.subheader('DIFFERENCES BETWEEN LAST CLOSE AND SMA21')
                temp_df=temp_df.sort_values(by=par,ascending=False)
                fig=px.bar(
                    temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800
                )
                #update the bar color
                bar_color_values=['lightgreen' if x>0 else 'coral' for x in temp_df[par]]
                #print(f'Debug: colors for bar {bar_color_values}')
                fig.update_traces(marker_color=bar_color_values)
                con_df=temp_df.copy()
            # elif sma_radio_option in [r'last_close-sma_50']:
                # temp_df['last_close-sma_50']=temp_df['last_close']-temp_df['sma_50']
                # st.subheader('DIFFERENCES BETWEEN LAST CLOSE AND SMA50')
                # temp_df=temp_df.sort_values(by='last_close-sma_50')
                # fig=px.bar(
                    # temp_df,x='ticker',y='last_close-sma_50',hover_data=hover_data,width=1600,height=800
                # )
                # con_df=temp_df.copy()
            # elif sma_radio_option in [r'last_close-sma_200']:
                # temp_df['last_close-sma_200']=temp_df['last_close']-temp_df['sma_200']
                # st.subheader('DIFFERENCES BETWEEN LAST CLOSE AND SMA200')
                # temp_df=temp_df.sort_values(by='last_close-sma_200')
                # fig=px.bar(
                    # temp_df,x='ticker',y='last_close-sma_200',hover_data=hover_data,width=1600,height=800
                # )
                # con_df=temp_df.copy()

#applying the session state for con_df for later use
st.session_state['dataframe']=con_df
fig.update_traces(hoverlabel=dict(bgcolor='lightblue',font_size=18,font_color='darkblue',font_family='monospace'))
fig.update_layout(
    font=dict(
        family="Arial",
        size=20,
        color="black"
    )
)
fig.update_layout(
    xaxis=dict(titlefont=dict(family="Arial Bold", size=20,color="black"),tickfont=dict(size=10,color='brown')),
    yaxis=dict(titlefont=dict(family="Arial Bold", size=20,color="black"))
)


st.plotly_chart(fig,use_container_width=True)
st.markdown("\ncontact info: bhattathakur2015@gmail.com")
