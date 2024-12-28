import os
from dotenv import load_dotenv
import qrcode
import hmac
import hashlib
import base64

# Load .env variables
load_dotenv()
key = os.getenv("QR_SECRET_KEY")


def generate_qrcode(member_id):
    data = f"{member_id}".encode('utf-8')
    # Create HMAC object and hash the data
    hmac_obj = hmac.new(key.encode('utf-8'), data, hashlib.sha512)  # Ensure key is encoded
    hashed_data = hmac_obj.digest()

    encoded_data = base64.urlsafe_b64encode(hashed_data).decode('utf-8')

    qr = qrcode.QRCode(  # Corrected the typo here
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4
    )

    qr.add_data(encoded_data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save('./qr_images/{}.png'.format(member_id))  # Ensure valid file path and extension



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

"""encoded_data_from_qr = "WnF4Xd7t9P0B23Wg26XBIpUtKO5T6yBJhsGD5C-MAHIzHf51eBw_HQMg0LElWI5cZlIgPVmfYZh017nLrj0kjw=="
member_id ='c729ca11-8018-4f46-8eb4-c2dfff162d09'

decode_and_verify_qr_data(encoded_data_from_qr, member_id)
"""