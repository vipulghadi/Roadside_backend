from rest_framework.response import Response
from rest_framework.exceptions import APIException
import re
import random
import string
from django.utils.text import slugify

def custom_response(success, message=None,data=None, errors=None, status=200):

    if errors:
        if isinstance(errors, dict):  
            first_field = next(iter(errors))
            first_error = errors[first_field][0]  
            errors =  first_error
    return Response({
        'message': message,
        'success': success,
        'data': data,
        'error': errors
    }, status=status)

        

def validate_phone_number(phone_number):
    pattern = r"^(?:\+91|91)?[789]\d{9}$"
    if re.match(pattern, phone_number):
        return True
    else:
        return False

def generate_slug(name):
    slug = slugify(name)
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    random_slug = f"{slug}-{random_string}"
    return random_slug