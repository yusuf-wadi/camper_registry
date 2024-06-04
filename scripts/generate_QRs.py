import pandas as pd
import segno

def generate_QR(data: tuple):
    identifier = f"{data[0]} {data[1]} {str(data[2])}"
    qrcode = segno.make_qr(identifier)
    # Save the image
    qr_name = identifier.split()[0] + '_' + identifier.split()[1] + '_' + str(identifier.split()[2]) + '.png'
    qrcode.save(f"./QRs/{qr_name}", scale = 6)
    
def generate_from_campers(df: pd.DataFrame):
    for index, row in df.iterrows():
        generate_QR((row['fname'], row['lname'], row['code']))
        
def main():
    df = pd.read_csv('./data/outputs/campers.csv')
    generate_from_campers(df)

main()