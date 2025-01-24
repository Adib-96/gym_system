import os
import sqlite3
from dotenv import load_dotenv
import qrcode
import hmac
import hashlib
import base64
from warehouse.database import insert_user_hmac
#! Load .env variables
load_dotenv()
key = os.getenv("QR_SECRET_KEY","waywa")


def generate_qrcode(member_id):
    
    
    if not key :
        raise ValueError('QR_SECRET_KEY not set in environment varibales.')
    
    
    data = f"{member_id}".encode('utf-8')
    # Create HMAC object and hash the data
    hmac_obj = hmac.new(key.encode('utf-8'), data, hashlib.sha512)  # Ensure key is encoded
    hashed_data = hmac_obj.digest()

    encoded_data = base64.urlsafe_b64encode(hashed_data).decode('utf-8')

    qr = qrcode.QRCode(  
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4
    )
    #? add this credentials to DB
    insert_user_hmac(member_id=member_id,encoded_data=encoded_data)
    
    #? ensure the qr_images exist
    os.makedirs('./qr_images',exist_ok=True)
    qr.add_data(encoded_data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save('./qr_images/{}.png'.format(member_id))  # Ensure valid file path and extension



#* call this function into the scan view module ( the encoded data input will be taken from phone and scan it with desktop Webcame)
def decode_and_verify_qr_data(encoded_data):
    sql_statment_to_extract_HMAC = "SELECT member_id FROM user_hmac WHERE HMAC=?"
    sql_statment_to_fetch_member_name = "SELECT name from members WHERE member_id=?"
    sql_statment_to_fetch_date_for_monthly_subscription = "SELECT subscription_end_date from subscriptions WHERE member_id=?"
    sql_statment_to_fetch_date_for_sessions_subscription = "SELECT remaining_sessions from subscriptions WHERE member_id=?"
    
    try:
        with sqlite3.connect('./warehouse.db') as conn:
            cursor = conn.cursor()
            cursor.execute(sql_statment_to_extract_HMAC,(encoded_data,))
            #!! user_id here will return a tuple
            user_id = cursor.fetchone()
            print("------------{}----------".format(user_id))
            ##? execute query to extract membername
            cursor.execute(sql_statment_to_fetch_member_name,(user_id[0],))
            member_name = cursor.fetchone()
            #? query to extract subscription_end_dat(Monthly)
            cursor.execute(sql_statment_to_fetch_date_for_monthly_subscription,(member_name,))
            end_date = cursor.fetchone()
            print(end_date or 0)
            cursor.execute(sql_statment_to_fetch_date_for_sessions_subscription,(member_name,))
            remaining_session =  cursor.fetchone()
            print(remaining_session or 0)
            
            if user_id is None:
                return "No matching record found for the provided HMAC."
            return member_name[0]
    
    except sqlite3.OperationalError as oe:
        print('Eroor ',oe)
