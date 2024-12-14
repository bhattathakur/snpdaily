import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")  # Enable wide mode


#reading information file
df=pd.read_csv('final_info_df.csv')

#last date saved in dataframe
last_date=df['last_date'].iloc[0]
last_day=pd.to_datetime(last_date).strftime('%A')
st.sidebar.info(f"RESULTS BASED ON {last_date}",icon="ℹ️")

#st.write(df)
#get labels and values
def get_labels_values(df_1,cut):
    temp_df=df_1.iloc[:,cut]
    labels=temp_df.columns.to_list()
    values=temp_df.iloc[0].to_list()
    show_text=True
    #if show_text:st.write(f'labels: {labels}')
    #if show_text:st.write(f'values: {values}')
    return labels,values

def check_if_values(values_list):
    """
    check if the list is empty or not 
    """
    return sum(values_list)>0


#create a function for pie-chart
def get_pie_charts(category,df=df):
    '''
    get pie charts for given category
    '''
    temp_df=df[df['category_name']==category]
    #st.write(f'temp_df:\n{temp_df}')
    gainer_labels,gainer_values=get_labels_values(temp_df,slice(1,3))
    sma5_labels,sma5_values=get_labels_values(temp_df,slice(3,5))
    close_labels,close_values=get_labels_values(temp_df,slice(5,7))
    rsi_labels,rsi_values=get_labels_values(temp_df,slice(7,9))
    high_labels,high_values=get_labels_values(temp_df,slice(9,11))
    up_labels,up_values=get_labels_values(temp_df,slice(11,13))
    #check values if exist for which will be used to determined if the pie chart is created for given label or not 
    check_gainer_values=check_if_values(gainer_values)
    check_close_smas_values=check_if_values(close_values)
    check_sma5_values=check_if_values(sma5_values)
    check_rsi_values=check_if_values(rsi_values)
    check_52week_values=check_if_values(high_values)
    check_3daysup_values=check_if_values(up_values)



    #colors
    colors=['lightgreen','salmon']
    marker=dict(colors=colors,line=dict(color='#000000',width=2))
    height=400
    width=400

    #container 1
    with st.container():
        #two columns
        col1,col2,col3=st.columns(3)

        #col1
        if check_gainer_values:
            with col1:
                pie1=go.Figure(data=[go.Pie(labels=gainer_labels,values=gainer_values,hole=0.3)])

                pie1.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
                title=f'GAINERS-LOSERS'
                pie1.update_layout(
                title={'text': f"{title}",'y': 0.9,'x': 0.35,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
                #pie1.update_layout(legend=dict(font=dict(size=18)))


                key=f"{category}_gainer"
                st.plotly_chart(pie1,key=key)
        #col2
        if check_close_smas_values:
            with col2:
                pie2=go.Figure(data=[go.Pie(labels=close_labels,values=close_values,hole=0.3)])
                pie2.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
                title=f'CLOSE AND SMAS'
                pie2.update_layout(
                title={'text': f"{title}",'y': 0.9,'x': 0.25,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
                key=f'{category}_close'
                #pie2.update_layout(legend=dict(font=dict(size=18)))
                st.plotly_chart(pie2,key=key)

        #col3
        if check_sma5_values:
            with col3:
                pie1=go.Figure(data=[go.Pie(labels=sma5_labels,values=sma5_values,hole=0.3)])
                pie1.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
                title=f'SMA5 & SMA10'
                pie1.update_layout(
                title={'text': f"{title}",'y': 0.9,'x': 0.3,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
                key=f'{category}_sma'
                st.plotly_chart(pie1,key=key)
    #con    tainter 2
    with st.container():
        col1,col2,col3=st.columns(3)

        if check_3daysup_values:
            with col1:
                pie1=go.Figure(data=[go.Pie(labels=up_labels,values=up_values,hole=0.3)])

                pie1.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
                title=f'3DAYS UP/DOWN'
                pie1.update_layout(
                title={'text': f"{title}",'y': 0.9,'x': 0.3,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
                key=f"{category}_updown"
                st.plotly_chart(pie1,key=key)
        if check_rsi_values:
            with col2:
                pie2=go.Figure(data=[go.Pie(labels=rsi_labels,values=rsi_values,hole=0.3)])
                pie2.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
                title=f'RSI>70 & RSI<30'
                pie2.update_layout(
                title={'text': f"{title}",'y': 0.9,'x': 0.3,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
                key=f'{category}_rsi'
                st.plotly_chart(pie2,key=key)
        if check_52week_values:
            with col3:
                pie3=go.Figure(data=[go.Pie(labels=high_labels,values=high_values,hole=0.3)])
                pie3.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
                title=f'52WEEK HIGHS/LOWS'
                pie3.update_layout(
                title={'text': f"{title}",'y': 0.9,'x': 0.3,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
                key=f'{category}_high'
                st.plotly_chart(pie3,key=key)

    
    #creating a list of lables and values for iterating the pie chart
    
    #df_gainer=temp_df.iloc[:,1:3]
    #labels=df_gainer.columns.to_list()
    #values=df_gainer.loc[0].to_list()
    #st.write(f'labels: {labels}')
    #st.write(f'values: {values}')
    #return None


debug=False
column_names=df.columns.to_list()

if debug:st.write(column_names)
if debug:st.write(df)

#used in the heading or etc
orgunique_categories=df['category_name'].to_list()

unique_categories=[x.upper() for x in orgunique_categories]

if debug:st.write(unique_categories)

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15=st.tabs(unique_categories)

#tab1
with tab1:
    tabno=1
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab2
with tab2:
    tabno=2
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    if debug:st.write(f'category: {cat}')
    #st.stop()
    get_pie_charts(cat)
#tab 3
with tab3:
    tabno=3
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 4
with tab4:
    tabno=4
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 5
with tab5:
    tabno=5
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 6
with tab6:
    tabno=6
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 7
with tab7:
    tabno=7
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 8
with tab8:
    tabno=8
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 9
with tab9:
    tabno=9
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 10
with tab10:
    tabno=10
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 11
with tab11:
    tabno=11
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 12
with tab12:
    tabno=12
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 13
with tab13:
    tabno=13
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 14
with tab14:
    tabno=14
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 15
with tab15:
    tabno=15
    cat=orgunique_categories[tabno-1]
    #st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}, {last_day}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
