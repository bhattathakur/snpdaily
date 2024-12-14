#loading different files as tabs 
import streamlit as st
# This must be the first Streamlit command
st.set_page_config(page_title="Multi-Tab App", layout="wide")

tab_list=['SCREENER','PIE_CHART','INFO_TABLE']
tab1,tab2,tab3=st.tabs(tab_list)
# Load example1.py content in Tab 1
with tab1:
    st.header(f"{tab_list[0]}")
    file='pages/1_📊SCREENER.py'
    with open(file) as f:
        code = f.read()
        exec(code)  # Executes the code inside example1.py

with tab2:
    st.header(f"{tab_list[1]}")
    file='pages/3_📀PIE_CHART.py'
    
    with open(file) as f:
        code = f.read()
        exec(code)  # Executes

with tab3:
    st.header(f"{tab_list[2]}")
    file='pages/1_📊SCREENER.py'
    with open(file) as f:
        code = f.read()
        exec(code)  # Executes the code inside example1.py

