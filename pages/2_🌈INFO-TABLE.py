import streamlit as st
st.set_page_config(layout='wide')

st.markdown("<h2 style='text-align:center;color:magenta'>Data Frame/Table based on the condition on the SCREENER</h2>",unsafe_allow_html=True)

#states from main page:
#st.write(f"""
#        sector_choice: {st.session_state['sector_choice']}
#        parameter_choice: {st.session_state['parameter_choice']}
#        sub-parameter_choice: {st.session_state['sub_parameter_choice']}
#        """)

if 'dataframe' in st.session_state:
    #st.write("Active session_state keys and values:")
    df=st.session_state['dataframe'].reset_index(drop=True) #dictionary
    #st.write(st.session_state)
    text_values_list=[]
    for key,value in st.session_state.items():
        if key=='dataframe':continue
        if value=='SMA-N-MISC':continue
        text_values_list.append(value)
        #st.write(f"{key}->{value}\n")
    #st.write(text_values_list)
    #text_values_text="|".join(text_values_list)
    info_text="".join(['| '+f'{i.upper()}'+' |' for i in text_values_list])
    df.index=range(1,len(df)+1)
    st.markdown(f"<h4 style='text-align:center;color:SlateBlue'>{info_text}</h4>",unsafe_allow_html=True)
    
    st.dataframe(df)
else:
    st.warning("PLEASE USE THE SCREENER FIRST",icon="⚠️")
