import os
from dotenv import load_dotenv
import qrcode
import hmac
import hashlib
import base64

#! Load .env variables
load_dotenv()
key = os.getenv("QR_SECRET_KEY","waywa")


def generate_qrcode(member_id):
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

    qr.add_data(encoded_data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save('./qr_images/{}.png'.format(member_id))  # Ensure valid file path and extension



#* call this function into the scan view module 
def decode_and_verify_qr_data(encoded_data,id_member):
    try:

        hashed_data = base64.urlsafe_b64decode(encoded_data)

        data = f'{id_member}'.encode('utf-8')
        expected_hmac= hmac.new(key.encode('utf-8'),data,hashlib.sha512).digest()

        if hashed_data == expected_hmac:
            print(f"QR code for {id_member} is correct.")
        else:
            print(f"QR code for {id_member} is not correct.")

    except Exception as e:
        print(f'Error during decoding or verification :{e}')



"""
? for testing purpose ;)
encoded_data_from_qr = "K2oKpTVKV8a694k-OH5CjCRIGZlgg2o4LGeUKpHHpyJY4GPEFIbag3UggpWrHlNSCTjQenOHnIWZkscbwGJUAQ=="
member_id= 'b0665f1f-ae52-44f8-bfcc-799515901993'


decode_and_verify_qr_data(encoded_data_from_qr, member_id)
"""