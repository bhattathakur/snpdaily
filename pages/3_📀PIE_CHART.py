import streamlit as st
#import plotly.graph_objects as go
import plotly.express as px
import numpy as np
st.set_page_config(layout='wide')

st.markdown("<h3 style='text-align:center;color:magenta'>Data Frame/Table based on the condition on the SCREENER</h3>",unsafe_allow_html=True)

#last date
last_date=st.session_state.get('last_date')
st.sidebar.info(f"RESULTS BASED ON {last_date}",icon="ℹ️")

# Function to boldface all text
def bold_text(df):
    return df.style.applymap(lambda x: f"font-weight: bold;")

# highlightcolor
def color_value(x):
    return f'color:green;' if x>0 else f'color:red;'

# Styling function to change text size, orientation, and weight
def style_cells(value):
    return 'font-size: 14px; font-weight: bold; text-align: center;'

    
debug=True
if 'dataframe' in st.session_state:
    #st.write("Active session_state keys and values:")
    df=st.session_state['dataframe'].reset_index(drop=True) #dictionary
    info_text=st.session_state.get('tabletitle')
    df.index=range(1,len(df)+1)#     + df['ticker']
    #new_index=df.index.astype(str)+'-'+df['ticker'].astype(str)
    #st.write(f'DEBUG: new_index: {new_index}')
    #df.index=new_index
    st.markdown(f"<h4 style='text-align:center;color:SlateBlue'>{info_text}</h4>",unsafe_allow_html=True)
    pie_df=df.copy().head(30)
    all_columns=pie_df.columns.to_list()
    yvalues=pie_df.iloc[:,1]
    fig=px.pie(pie_df,values=yvalues.abs().round(2),names='ticker',hover_data=[all_columns[1]])
    fig.update_traces(textposition='inside',textinfo='label')
    fig.update_traces(hovertemplate='%{label}<extra></extra>')
    # Customize hover template to include label and second column
    fig.update_traces(
    hovertemplate='TICKER: %{label}<br>'+all_columns[1].upper()+': %{customdata[0]}<extra></extra>',
    customdata=pie_df[all_columns[1]].round(2)# Pass the second column to customdata
    )
    fig.update_layout(width=800,height=800)
    fig.update_layout(
    hoverlabel=dict(
        bgcolor="lightblue",
        font_size=18,
        font_color='darkblue',
        font_family="Rockwell"
    )
   )

    st.plotly_chart(fig,use_container_width=True)
    
    #if(debug):st.write(f'z: {z}')
    #all_cols={'font-size:15px;font-weight:bold;text-align:center;'}
    #yellow_highlight={'background-color':'yellow'}
    #green_highlight={'background-color':'#4285F4'}
    #secondcol_highlight={'background-color':'#ffffcc','font-weight':'35px'}
    #yellow_columns=[i for i in all_columns if i.startswith('sma')]
    #color_columns=[i for i in all_columns if 'change' in i]
    ##st.dataframe(df.style\
    #        #.applymap(style_cells)\
    #        .set_properties(subset=yellow_columns,**yellow_highlight)\
    #        .set_properties(subset=['ticker'],**green_highlight)\
    #        .set_properties(subset=[all_columns[1]],**yellow_highlight)\
    #        .map(color_value,subset=color_columns)\
    #        .format(precision=2),use_container_width=True,height=600)
    #st.dataframe(df.style.set_properties(subset=['ticker'],**green_highlight).format(precision=2))
    #st.markdown(df,unsafe_allow_html=True)
    
    #st.dataframe(df.style.background_gradient(axis=None).format(precision=2))
else:
    st.warning("PLEASE USE THE SCREENER FIRST",icon="⚠️")
