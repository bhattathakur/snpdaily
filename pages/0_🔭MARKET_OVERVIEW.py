import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")  # Enable wide mode
last_date=st.session_state.get('last_date')
st.sidebar.info(f"RESULTS BASED ON {last_date}",icon="ℹ️")


#reading information file
df=pd.read_csv('final_info_df.csv')

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

    #colors
    colors=['lightgreen','salmon']
    marker=dict(colors=colors,line=dict(color='#000000',width=2))
    height=400
    width=400

    #container 1
    with st.container():
        #two columns
        col1,col2=st.columns(2)

        #col1
        with col1:
            pie1=go.Figure(data=[go.Pie(labels=gainer_labels,values=gainer_values,hole=0.3)])

            pie1.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
            title=f'GAINERS-LOSERS'
            pie1.update_layout(
            title={'text': f"{title}",'y': 0.9,'x': 0.4,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
            key=f"{category}_gainer"
            st.plotly_chart(pie1,key=key)
        #col2
        with col2:
            pie2=go.Figure(data=[go.Pie(labels=close_labels,values=close_values,hole=0.3)])
            pie2.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
            title=f'CLOSE AND SMAS'
            pie2.update_layout(
            title={'text': f"{title}",'y': 0.9,'x': 0.3,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
            key=f'{category}_close'
            st.plotly_chart(pie2,key=key)


    #containter 2
    with st.container():
        col1,col2,col3=st.columns(3)

        #col1
        with col1:
            pie1=go.Figure(data=[go.Pie(labels=sma5_labels,values=sma5_values,hole=0.3)])
            pie1.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
            title=f'SMA5 & SMA10'
            pie1.update_layout(
            title={'text': f"{title}",'y': 0.9,'x': 0.3,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
            key=f'{category}_sma'
            st.plotly_chart(pie1,key=key)
        with col2:
            pie2=go.Figure(data=[go.Pie(labels=rsi_labels,values=rsi_values,hole=0.3)])
            pie2.update_traces(hoverinfo='label+value',textinfo='percent',marker=marker,textfont_size=20)
            title=f'RSI>70 & RSI<30'
            pie2.update_layout(
            title={'text': f"{title}",'y': 0.9,'x': 0.4,'xanchor': 'center', 'yanchor': 'top'},height=height,width=width)
            key=f'{category}_rsi'
            st.plotly_chart(pie2,key=key)
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
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab2
with tab2:
    tabno=2
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    if debug:st.write(f'category: {cat}')
    #st.stop()
    get_pie_charts(cat)
#tab 3
with tab3:
    tabno=3
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 4
with tab4:
    tabno=4
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 5
with tab5:
    tabno=5
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 6
with tab6:
    tabno=6
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 7
with tab7:
    tabno=7
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 8
with tab8:
    tabno=8
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 9
with tab9:
    tabno=9
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)

#tab 10
with tab10:
    tabno=10
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 11
with tab11:
    tabno=11
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 12
with tab12:
    tabno=12
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 13
with tab13:
    tabno=13
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 14
with tab14:
    tabno=14
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
#tab 15
with tab15:
    tabno=15
    cat=orgunique_categories[tabno-1]
    st.markdown(f"<h4 Style='text-align:center;background-color:Silver;color:blue';>{cat.upper()} OVERVIEW ON {last_date}</h4>",unsafe_allow_html=True)
    get_pie_charts(cat)
