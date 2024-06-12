import cv2
import numpy as np
import streamlit as st
import time
import pandas as pd
import os

GLOBAL_DATE = time.strftime("%Y-%m-%d")

def create_sheet():
    date = GLOBAL_DATE
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
    date = GLOBAL_DATE
    df = pd.read_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv')
    # add points to the camper, change present to True
    df.loc[(df['fname'] == pk[0]) & (df['lname'] == pk[1]), 'points'] += data[2]
    df.loc[(df['fname'] == pk[0]) & (df['lname'] == pk[1]), 'present'] = True
    df.to_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv', index=False)
    return df

def load_qr():
    image = st.camera_input("Show QR code")
    if image is not None:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        detector = cv2.QRCodeDetector()

        data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)
        return data
    
def ret_camper_from_code(code):
    code = int(code)
    df = pd.read_csv('./data/outputs/campers.csv')
    # get fname and lname from code
    camper = df.loc[df['code'] == code]
    print(camper)
    return camper

def add_camper(fname, lname):
    current_campers = pd.read_csv('./data/outputs/campers.csv')
    code = current_campers['code'].max() + 1
    while code in current_campers['code']:
        code += 1
    current_campers.loc[len(current_campers)] = [fname, lname, code, 0, False]
    current_campers.to_csv('./data/outputs/campers.csv', index=False)
    #update attendance sheet
    date = GLOBAL_DATE
    df = pd.read_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv')
    df.loc[len(df)] = [fname, lname, code, 0, False]
    df.to_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv', index=False)

def calc_points(current_time):
    if current_time <= "11:00:00":
        return 10
    # 1-10mins late: 5pts
    elif current_time <= "11:10:00":
        return 5
    else:
        return 0
    
def rem_dups():
    date = GLOBAL_DATE
    dfs = [pd.read_csv('./data/outputs/campers.csv'), pd.read_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv')]
    for df in dfs:
        df.dropna(inplace=True)
        df.drop_duplicates(subset=['fname', 'lname'], keep='first', inplace=True)
        df.to_csv('./data/outputs/campers.csv', index=False)
        df.to_csv('./data/outputs/attendance/rijaal_attendance.csv', index=False)
             
def app():
    rem_dups()
    attendance_sheet = pd.read_csv('./data/outputs/attendance/rijaal_attendance.csv')
    df = attendance_sheet
    date = GLOBAL_DATE
    data = load_qr()
    selection = st.selectbox("choose an option", ["check in camper", "register camper"])
    match(selection):
        case "check in camper": 
            if data:
                camper = data.split()
                points = calc_points(date)
                df = update_sheet((camper[0], camper[1], points))
                st.write(f"{camper[0]} {camper[1]} has been marked present with {points} points")
            # show attendance sheet
            code = st.text_input("Enter code")
            if code:
                camper = ret_camper_from_code(code)
                points = calc_points(time.strftime("%H:%M:%S"))
                df = update_sheet((camper['fname'].values[0], camper['lname'].values[0], points))
                st.success(f"{camper['fname'].values[0]} {camper['lname'].values[0]} has been marked present with {points} points")
        case "register camper":
            new_camper = st.form("Add new camper")
            nc_fname = new_camper.text_input("Enter first name")
            nc_lname = new_camper.text_input("Enter last name")
            new_camper.form_submit_button("Add camper", on_click=add_camper, args=(nc_fname, nc_lname))
            df = pd.read_csv(f'./data/outputs/attendance/rijaal_attendance_{date}.csv')
    st.write(df)
    
create_sheet()      
app()