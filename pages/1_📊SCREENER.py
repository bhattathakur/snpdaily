#loading different files as tabs 
import streamlit as st
# This must be the first Streamlit command
st.set_page_config(page_title="SCREENER", layout="wide")

tab_list=['📊BAR_CHART','📀PIE_CHART','📝INFO_TABLE']
tab1,tab2,tab3=st.tabs(tab_list)
# Load example1.py content in Tab 1
with tab3:
    #st.header(f"{tab_list[0]}")
    file='pyfiles/SCREENER.py'
   
    
    with open(file,'r',encoding='utf-8') as f:
        code = f.read()
        exec(code)  # Executes the code inside example1.py

with tab2:
    #st.header(f"{tab_list[1]}")
    file='pyfiles/3_📀PIE_CHART.py'
    
    with open(file,'r',encoding='utf-8') as f:
        code = f.read()
        exec(code)  # Executes

with tab1:
    #st.header(f"{tab_list[2]}")
    file='pyfiles/2_🌈INFO_TABLE.py'
    with open(file,'r',encoding='utf-8') as f:
        code = f.read()
        exec(code)  # Executes the code inside INFO_TABLE.py