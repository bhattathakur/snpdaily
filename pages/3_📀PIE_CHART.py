import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
#st.set_page_config(layout='wide')

st.markdown("<h6 style='text-align:center;color:magenta'>PIE CHART  based on the condition on the SCREENER</h6>",unsafe_allow_html=True)

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
    #st.write(f'all_columns: {all_columns}')
    #hover_text
    #st.stop()
    condition='ipo_year' in all_columns
    #st.write(f'condition: {condition}')
    if condition:
        ipo_year_idx=pie_df.columns.get_loc('ipo_year')
    #if 'ipo_year' in pie_df.all_columns:
    pie_df['hover_text']=(
            'TICKER: '+pie_df.iloc[:,0]+'<br>'
            +all_columns[1].upper()+' : '+pie_df[all_columns[1]].round(2).astype(str)+'<br>'
            +(all_columns[ipo_year_idx].upper()+' : '+pie_df[all_columns[ipo_year_idx]].astype(str) if condition else '')
            )
    #pie_df['hover_text']=pie_df[all_columns[ipo_year_idx]].astype(str)if condition else ''
    #st.write(pie_df)
    #st.stop()

    yvalues=pie_df.iloc[:,1]
    #hover_text=pie_df['hover_text']
    second_col=all_columns[1]
    #names-> label,values->sector 
    fig=go.Figure(
            data=[
                go.Pie(
                    labels=pie_df['ticker'],values=yvalues.abs(),
                    textinfo='label',hole=0.5,hoverinfo=None,
                    hovertemplate='%{customdata}<extra></extra>',
                    customdata=pie_df['hover_text']
                    )
                ]
            
            )
    font_size=20
    if len(info_text)>40:
        font_size=12
    fig.add_annotation(
        text=f"{info_text}",  # Text to display in the center
        x=0.5,  # X position (0.5 places it in the center of the chart)
        y=0.5,  # Y position (0.5 places it in the center of the chart)
        font=dict(size=font_size, color="brown"),  # Font size and color
        showarrow=False  # Disable the arrow pointing to the text
    )
    size=750
    fig.update_layout(width=size,height=size)
    fig.update_layout(
    hoverlabel=dict(
        bgcolor="lightblue",
        font_size=18,
        font_color='darkblue',
        font_family="Rockwell"
    )
   )

    st.plotly_chart(fig,use_container_width=True)
else:
    st.warning("PLEASE USE THE SCREENER FIRST",icon="⚠️")
