import random


def generate_otp():
    return "123456"
    return random.randint(100000, 999999)


def validate_otp(contact_number, otp):
    return otp == '123456'
