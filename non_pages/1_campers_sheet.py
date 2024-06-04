import pandas as pd
import streamlit as st
import os
import time

# create todays sheet, if it doesn't exist
def create_sheet():
    date = time.strftime("%Y-%m-%d")
    if not os.path.exists(f'./data/outputs/attendance/rijaal_attendance_{date}.csv'):
        df = pd.DataFrame(columns=['fname', 'lname', 'code', 'points', 'present'])
        df.to_csv(f'./data/outputs/rijaal_attendance_{date}.csv', index=False)
        
def page():
    create_sheet()
    st.title('Campers Sheet')
    st.write('This is the campers sheet page')
    st.write('Here you can see and edit the campers sheet')
    st.write('You can also add new campers')
    
    date = time.strftime("%Y-%m-%d")
    
    df = pd.read_csv(f'./data/outputs/rijaal_attendance_{date}.csv')
    st.write(df)
    
page()