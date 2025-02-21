import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

#st.set_page_config(layout="wide")  # Enable wide mode


#data files sources
files_list={
'SNP500':'df_snp500.csv',
'SNP500-SECTOR':'df_snp500.csv',
'NASDAQ100':'df_nasdaq100.csv',
'DOW':'df_dow.csv',
'IPO':'df_nasdaqipo.csv'
}

#if 'index_key' not in st.session_state:
#    st.session_state["index_key"]= "SNP500"  # Default selection
#if 'parameter_key' not in st.session_state:
#    st.session_state["parameter_key"] = "Gainer"  # Default parameter choice
#if 'daterange_key' not in st.session_state:
#    st.session_state["daterange_key"]= "last_day"  # Default sub-parameter
#if 'sector_key' not in st.session_state:
#    st.session_state["sector_key"]= ""  # Default sub-parameter
#if 'misc_key' not in st.session_state:
#    st.session_state["misc_key"]= ""  # Default sub-parameter
#if 'dataframe' not in st.session_state:
#    st.session_state["dataframe"]= ""  # Default sub-parameter

#if 'misc_parameter_choice' not in st.session_state:
#    st.session_state["misc_parameter_choice"] = r'last_close > sma_50 & last_close > sma_200'

title_template="|| "

side_bar_selection=st.sidebar.selectbox('select an option',files_list.keys(),key='index_key')
if side_bar_selection:title_template+=side_bar_selection+" || "

st.session_state['sidebar_choice']=side_bar_selection #SESSION_STATE
#if 'sector_choice' not in st.session_state:
#    st.session_state["sector_choice"]= side_bar_selection  # Default selection

#print(f'Debug:key:sector_choice: {st.session_state.sector_choice}')

#print(f'Debug:side_bar_selection: {side_bar_selection}') 


#load master df
data_file=files_list[side_bar_selection]
#print(f'Debug: data_file: {data_file}')
df_main=pd.read_csv(data_file) #read a file

#change up_3_days and down_3_days into bool
#already bool now
#df_main['up_3_days']=df_main['up_3_days'].astype(bool)
#df_main['down_3_days']=df_main['down_3_days'].astype(bool)

#print head of a file
#st.write(df_main.head(5))
#st.stop()
#check 52 two week high and low
df_main['fiftytwoweek_low']=(df_main['last_close']==df_main['fiftytwo_week_low'])
df_main['fiftytwoweek_high']=(df_main['last_close']==df_main['fiftytwo_week_high'])

last_date=df_main['last_date'].values[0]
last_day=pd.to_datetime(last_date).strftime('%A') #last day
#store last_date in st.session for use
st.session_state['last_date']=last_date
#print(f'Debug: Last Date: {last_date}')
#st.header(f'SNP500 OVERVIEW [{last_date}]')
st.markdown(
f"<h4 style='text-align:center'> {side_bar_selection} OVERVIEW [{last_date}, {last_day}]</h4>",
unsafe_allow_html=True
)

#cteate a stramlit 
hover_data=['ticker','last_close','last_change_pct','last_change','last_volume(M)','sma_21','sma_50','sma_200',\
            'fiftytwo_week_high','fiftytwo_week_low','pct_change_latest_week','pct_change_latest_month','pct_change_latest_year']

if side_bar_selection=='SNP500-SECTOR':
    sectors_list=pd.unique(df_main['sector']) #select a sector
    #print(f"Debug: {sectors_list}")
    sector_selection=st.sidebar.selectbox('select a sector',sectors_list,index=1,key='sector_key')
    if sector_selection:title_template+=sector_selection+" || "
    #if 'sector' not in st.session_state:
    st.session_state["sector_choice"]=sector_selection  # Default selection #
    #print(f'Debug: sector selection: {sector_selection}')
    #print(f"Debug: sector key: {st.session_state['sector']}")
    st.markdown(
        f"<h5 style='text-align:center;color:darkorchid;'>{sector_selection}</h5>",
        unsafe_allow_html=True
    )
    temp_df=df_main[df_main['sector']==sector_selection].reset_index(drop=True)
    #st.write(sector_df)

if side_bar_selection in ['SNP500','NASDAQ100','DOW','IPO']:
    temp_df=df_main.copy()
    #also change the hover_data if IPO
    if side_bar_selection in ['IPO']:
        hover_data.insert(5,'ipo_year')
        #pop the ipo year column
        popped_col=temp_df.pop('ipo_year').astype(int)
        temp_df.insert(5,'ipo_year',popped_col)





#function to display the dataframe based on the option chosen need to change later for %
def get_filtered_df(condition,ascending=True,df=temp_df):
    d=df.sort_values(by=condition,ascending=ascending).reset_index(drop=True)
    return d

#get new df with selected change at position 1 after ticker by default
#@st.cache_data
def get_changed_df(df,parameter,new_index=1):
    popped_column=df.pop(parameter) #inplace
    #insert popped column in df
    df.insert(1,parameter,popped_column)
    return df


gainer_loser_key_values={\
    'last_day':'last_change_pct',\
    'this_week':'pct_change_latest_week',
    'this_month':'pct_change_latest_month',
    'ytd':'pct_change_latest_year'
}

#st.sidebar.text('contact: bhattathakur2015@gmail.com')
if side_bar_selection in ['SNP500','SNP500-SECTOR','DOW','NASDAQ100','IPO']:
#gainer loser selection in side bar
    parameter_selection=st.sidebar.radio('Parameters:',['Gainer','Loser','SMA-N-MISC'],key='parameter_key')
    if parameter_selection in ['Gainer','Loser']:title_template+=parameter_selection+" || "
    #if 'parameter_choice' not in st.session_state:
    st.session_state["parameter_choice"]=parameter_selection# Default sub-parameter

    if parameter_selection in ['Gainer','Loser']:
        gainer_radio_option=st.sidebar.radio(
       'time_range:',
        ('last_day','this_week','this_month','ytd'),key='daterange_key')
        #print(f'Debug:parameter-button: {parameter_selection} radio_option: {gainer_radio_option}')
        if gainer_radio_option:title_template+=gainer_radio_option+" || "

        #if 'date_range_choice' not in st.session_state:
        st.session_state["daterange_choice"]=gainer_radio_option  # Default sub-parameter

        #print(f"Debug: gainer_radio_key{st.session_state.date_range_choice}")
        condition=gainer_loser_key_values[gainer_radio_option]
        #print(f'condition: {condition}')
        ascending=True
        if parameter_selection=='Gainer':ascending=False
        con_df=get_filtered_df(condition=condition,ascending=ascending)

        #looking for an alternative
        if parameter_selection=='Gainer':
            con_df=temp_df[temp_df[condition]>0].sort_values(by=condition,ascending=False)
        if parameter_selection=='Loser':
            con_df=temp_df[temp_df[condition]<0].sort_values(by=condition,ascending=True)
        con_df=get_changed_df(con_df,condition) #NOTE: This is a change 

        top_show=30
        plot_con_df=con_df.copy().head(top_show) #Top 20 
        #if number of rows available is less than top_show
        top_show=len(plot_con_df)

        #modify colors to bars
        colors=['lightgreen' if value>=0 else 'salmon' for value in plot_con_df[condition]]

        #print(f"Debug: colors: {colors}")

        #title for gainer loser
        header_text=f'{side_bar_selection}-{parameter_selection.upper()}-{gainer_radio_option.upper()} [TOP: {top_show}]'
        header_color='green' if 'GAINER' in header_text else 'red'
        #st.subheader(f'{parameter_selection.upper()}-{gainer_radio_option.upper()}')
        st.markdown(
    f"<h5 style='text-align: center;color:{header_color};'>{header_text}</h5>",
    unsafe_allow_html=True
)

        fig=px.bar(
            plot_con_df,x='ticker',y=condition,hover_data=hover_data,width=1600,height=800,text_auto=True
        )
        fig.update_traces(marker_color=colors)


    if parameter_selection in ['SMA-N-MISC']:
        #if 'misc_parameter_choice' not in st.session_state:
        #    st.session_state.misc_parameter_choice = r'last_close > sma_50 & last_close > sma_200'
        apply_conditions=[
            r'last_close > sma_50 & last_close > sma_200',\
            r'last_close < sma_50 & last_close < sma_200',\
            r'sma_5 > sma_10',\
            r'sma_5 < sma_10',\
            r'fiftytwoweek_high',r'fiftytwoweek_low',\
            f'up_3_days',\
            f'down_3_days',\
            f'gapped_up',\
            f'gapped_down'
        ]
        other_conditions=[
            #r'fiftytwo_week_high',r'fiftytwo_week_low',\
            r'highest_volume',\
            r'highest_atr%',\
            r'highest_rsi',\
            r'last_close-sma_5', r'last_close-sma_10',r'last_close-sma_21', r'last_close-sma_50',r'last_close-sma_200',\
        ]
        radio_option_list=apply_conditions+other_conditions
        sma_radio_option=st.sidebar.radio( 'Features:', radio_option_list,key='misc_key')
        if sma_radio_option:title_template+=sma_radio_option+" ||"
        #print(f'parameter-button: {parameter_selection} radio_option: {sma_radio_option}')
        #if 'misc_parameter_choice' not in st.session_state:
        st.session_state["misc_choice"] = sma_radio_option  #r'last_close > sma_50 & last_close > sma_200'

        #checking if the option is inside the sma_radio_option
        if sma_radio_option in apply_conditions:
            #print(f'Debug: inside apply_condition')
            #if gapped_up or down use the gap
            if(sma_radio_option=='gapped_up'):
                con_df=temp_df.query('gap>0').sort_values(by='gap',ascending=False)
                #length of the dataframe or head 20 what ever is bigger
                lenght_of_df=len(con_df)
                head=30 if lenght_of_df>20 else lenght_of_df
                con_df=con_df.head(head)
                txt=f' [TOP: {head}]'

                #inserting gap in second position
                con_df.insert(1,'opening_gap',con_df.pop('gap'))
                #assining y=opening_gap 
                y='opening_gap' #for bar diagram
            elif(sma_radio_option=='gapped_down'):
                con_df=temp_df.query('gap<0').sort_values(by='gap',ascending=True)
                #length of the dataframe or head 20 what ever is bigger
                lenght_of_df=len(con_df)
                head=30 if lenght_of_df>20 else lenght_of_df
                con_df=con_df.head(head)
                txt=f' [TOP: {head}]'
                #inserting gap in second position
                con_df.insert(1,'opening_gap',con_df.pop('gap'))
                y='opening_gap'
            else:
                con_df=temp_df.query(sma_radio_option).sort_values(by='last_close').reset_index(drop=True)
                txt=f' [ALL]'
                y='last_close'
            #st.subheader(f'{sma_radio_option.upper()}')

            #NOTE: using the index position to give the color of the bar plots
            index_of_radio_option=apply_conditions.index(sma_radio_option)
            #print(f'Debug: index_of_radio_option: {index_of_radio_option}')
            h2_color='SlateBlue' #'red' if 'down' or 'low' in sma_radio_option else 'lightgreen'
            marker_color='red' if index_of_radio_option%2==1  else 'lightgreen'
            
            st.markdown(
                f"<h2 style='text-align:center;color:{h2_color};background-color:rgb(255, 230, 179,0.25);padding:3px'>{sma_radio_option.upper()}{txt}</h2>",
                unsafe_allow_html=True
                        )
            plot_con_df=con_df.copy()
            fig=px.bar(
             plot_con_df,x='ticker',y=y,hover_data=hover_data,width=1600,height=800,text_auto=True,
            )
            fig.update_traces(marker_color=marker_color)

        else:# sma_radio_option in [r'last_close-sma_21', r'last_close-sma_50',r'last_close-sma_200',r'up_three_days']:
            top=40
            if sma_radio_option in [r'highest_volume']:
                par='last_volume(M)'
                st.markdown(f"<h3 style='text-align:center;color:OliveDrab'>HIGHEST {par.upper()} [TOP {top}]</h3>",unsafe_allow_html=True)
                temp_df=temp_df.sort_values(by=par,ascending=False).head(top)
                fig=px.bar(temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800,text_auto=True)
                con_df=temp_df.copy()
                con_df=get_changed_df(con_df,par)

            elif sma_radio_option in [r'highest_atr%']:
                par='atr%'
                st.markdown(f"<h3 style='text-align:center;color:OliveDrab'>HIGHEST {par.upper()} [ATR w.r.t. CLOSE, TOP {top}]</h3>",unsafe_allow_html=True)
                temp_df=temp_df.sort_values(by=par,ascending=False).head(top)
                fig=px.bar(temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800,text_auto=True)
                con_df=temp_df.copy()
                con_df=get_changed_df(con_df,par)
            elif sma_radio_option in [r'highest_rsi']:
                par='rsi'
                st.markdown(f"<h3 style='text-align:center;color:OliveDrab'>HIGHEST {par.upper()} [TOP {top}]] ",unsafe_allow_html=True)
                temp_df=temp_df.sort_values(by=par,ascending=False).head(top)
                fig=px.bar(temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800,text_auto=True)
                con_df=temp_df.copy()
                con_df=get_changed_df(con_df,par)

            elif sma_radio_option in [r'last_close-sma_5',r'last_close-sma_10',r'last_close-sma_21',r'last_close-sma_50',r'last_close-sma_200']:
                how_many=20
                par=sma_radio_option
                sma_part=par.split('-')[1]
                last_close_part=par.split('-')[0]
               #print(f"Debug: sma_radio_option: {par}\n sma_part: {sma_part}")
                temp_df[par]=temp_df['last_close']-temp_df[sma_part]
                #Break into two parts 3 lines added
                part1=temp_df.sort_values(by=par,ascending=True).head(how_many) #twenty lower
                part2=temp_df.sort_values(by=par,ascending=False).head(how_many) #twenty upper
                temp_df=pd.concat([part1,part2],axis=0).reset_index(drop=True).round(2) #rounded to two digits
                #temp_df['last_close-sma_21']=temp_df['last_close']-temp_df['sma_21']
                st.markdown(
                    f"<h2 style='text-align:center;color:magenta'>{par.upper()} [TOP-{how_many}]</h2>",unsafe_allow_html=True
                )
                #st.subheader('DIFFERENCES BETWEEN LAST CLOSE AND SMA21')
                temp_df=temp_df.sort_values(by=par,ascending=False)
                fig=px.bar(
                    temp_df,x='ticker',y=par,hover_data=hover_data,width=1600,height=800,text_auto=True
                )
                #update the bar color
                bar_color_values=['lightgreen' if x>0 else 'coral' for x in temp_df[par]]
                #print(f'Debug: colors for bar {bar_color_values}')
                fig.update_traces(marker_color=bar_color_values)
                con_df=temp_df.copy()
                con_df=get_changed_df(con_df,par)
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

#find the string for data table

#st.write(f"{title_template.upper()}")
#side bar with information about the last trading day and current time
st.sidebar.info(f"RESULTS BASED ON {last_date}",icon="ℹ️")


st.session_state['dataframe']=con_df
st.session_state['tabletitle']=title_template.upper()

#st.session_state['fig']=fig
#fig=st.session_state['fig']
fig.update_layout(yaxis_title=fig.layout.yaxis.title.text.upper(),xaxis_title=fig.layout.xaxis.title.text.upper())

fig.update_traces(hoverlabel=dict(bgcolor='lightblue',font_size=18,font_color='darkblue',font_family='monospace'))
fig.update_layout(
    font=dict(
        family="Arial",
        size=20,
        color="black"
    )
)
template='plotly_dark'
fig.update_layout(
        template=template,
    xaxis=dict(title=dict(family="Arial Bold", size=20,color="cyan"),tickfont=dict(family='Times New Roman,bold',size=15,color='brown')),
    yaxis=dict(title=dict(family="Arial Bold", size=20,color="cyan"))
)
yaxis_title=fig.layout.yaxis.title.text
#fig.update_layout(yaxis_title=fig.layout.yaxis.title.text.upper(),xaxis_title=fig.layout.xaxis.title.text.upper())
#print(f'yaxis_title:{yaxis_title}')
fig.update_layout(width=1200,height=680)


st.plotly_chart(fig,use_container_width=True)
st.markdown("\ncontact info: bhattathakur2015@gmail.com")
