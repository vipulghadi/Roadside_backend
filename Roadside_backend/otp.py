import pyotp # type: ignore
import hashlib
import base64

def generate_secret_key(contact_number):
    hashed_contact = hashlib.sha256(contact_number.encode()).hexdigest()
    secret_key = base64.b32encode(hashed_contact[:16].encode()).decode()
    return secret_key 



def generate_otp(contact_number):
    secret_key = generate_secret_key(contact_number) 
    totp = pyotp.TOTP(secret_key, interval=60)
    return totp.now()  


def validate_otp(contact_number, otp):
    secret_key = generate_secret_key(contact_number) 
    totp = pyotp.TOTP(secret_key, interval=60)
    
    return totp.verify(otp) 

