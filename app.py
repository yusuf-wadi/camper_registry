import cv2
import numpy as np
import streamlit as st
import time
import pandas as pd
import os

def create_sheet():
    date = time.strftime("%Y-%m-%d")
    if not os.path.exists(f'./data/outputs/attendance/rijaal_attendance_{date}.csv'):
        df = pd.DataFrame(columns=['fname', 'lname', 'code', 'points', 'present'])
        campers = pd.read_csv('./data/outputs/campers.csv')
        df['fname'] = campers['fname']
        df['lname'] = campers['lname']
        df['code'] = campers['code']
        df['points'] = 0
        df['present'] = False    
        df.to_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv', index=False)
        
def update_sheet(data: tuple):
    pk = (data[0], data[1])
    date = time.strftime("%Y-%m-%d")
    df = pd.read_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv')
    # add points to the camper, change present to True
    df.loc[(df['fname'] == pk[0]) & (df['lname'] == pk[1]), 'points'] += data[2]
    df.loc[(df['fname'] == pk[0]) & (df['lname'] == pk[1]), 'present'] = True
    df.to_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv', index=False)

def load_qr():
    image = st.camera_input("Show QR code")
    if image is not None:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()

        data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

        st.write("Here!")
        st.write(data)
        return data
    
def ret_camper_from_code(code):
    print(code)
    df = pd.read_csv('./data/outputs/campers.csv')
    # get first name and last name of camper as tuple
    camper = df[df['code'] == code]
    return camper
   
def calc_points(current_time):
    if current_time <= "11:00:00":
        return 10
    # 1-10mins late: 5pts
    elif current_time <= "11:10:00":
        return 5
    else:
        return 0
            
def app():
    data = load_qr()
    points = 0
    if data:
        camper = data.split()
        points = calc_points(time.strftime("%H:%M:%S"))
        update_sheet((camper[0], camper[1], points))
        st.write(f"{camper[0]} {camper[1]} has been marked present with {points} points")
    # show attendance sheet
    date = time.strftime("%Y-%m-%d")
    df = pd.read_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv')
    
    st.write(df)
    
create_sheet()      
app()