import streamlit as st
st.set_page_config(layout='wide')

st.markdown("<h2 style='text-align:center;color:magenta'>Data Frame/Table based on the condition on the SCREENER</h2>",unsafe_allow_html=True)

if 'dataframe' in st.session_state:
    df=st.session_state['dataframe'].reset_index(drop=True)
    df.index=range(1,len(df)+1)
    st.dataframe(df)
else:
    st.write("PLEASE USE THE SCREENER FIRST")
