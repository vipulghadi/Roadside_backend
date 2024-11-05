import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError


def is_valid_contact_number(contact_number):
    # Allow optional '+' at the beginning and require 10-15 digits
    return bool(re.match(r'^\+?\d{10,15}$', contact_number))


def is_valid_email(email):
    email_validator = EmailValidator()
    try:
        email_validator(email)
        return True
    except DjangoValidationError:
        return False

