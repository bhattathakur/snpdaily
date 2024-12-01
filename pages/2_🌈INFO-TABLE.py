import streamlit as st
import numpy as np
st.set_page_config(layout='wide')

st.markdown("<h2 style='text-align:center;color:magenta'>Data Frame/Table based on the condition on the SCREENER</h2>",unsafe_allow_html=True)

# Function to boldface all text
def bold_text(df):
    return df.style.applymap(lambda x: f"font-weight: bold;")

# highlightcolor
def color_value(x):
    return f'color:green;' if x>0 else f'color:red;'

# Styling function to change text size, orientation, and weight
def style_cells(value):
    return 'font-size: 14px; font-weight: bold; text-align: center;'

    

if 'dataframe' in st.session_state:
    #st.write("Active session_state keys and values:")
    df=st.session_state['dataframe'].reset_index(drop=True) #dictionary
    info_text=st.session_state.get('tabletitle')
    df.index=range(1,len(df)+1)
    all_columns=df.columns.to_list()
    st.markdown(f"<h4 style='text-align:center;color:SlateBlue'>{info_text}</h4>",unsafe_allow_html=True)
    all_cols={'font-size:15px;font-weight:bold;text-align:center;'}
    yellow_highlight={'background-color':'yellow'}
    green_highlight={'background-color':'#4285F4'}
    secondcol_highlight={'background-color':'#ffffcc','font-weight':'35px'}
    yellow_columns=[i for i in all_columns if i.startswith('sma')]
    color_columns=[i for i in all_columns if 'pct' in i]
    st.dataframe(df.style\
            #.applymap(style_cells)\
            .set_properties(subset=yellow_columns,**yellow_highlight)\
            .set_properties(subset=['ticker'],**green_highlight)\
            .set_properties(subset=[all_columns[1]],**yellow_highlight)\
            .map(color_value,subset=color_columns)\
            .format(precision=2))
    #st.dataframe(df.style.set_properties(subset=['ticker'],**green_highlight).format(precision=2))
    #st.markdown(df,unsafe_allow_html=True)
    
    #st.dataframe(df.style.background_gradient(axis=None).format(precision=2))
else:
    st.warning("PLEASE USE THE SCREENER FIRST",icon="⚠️")
