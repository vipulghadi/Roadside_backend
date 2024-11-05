from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

@shared_task
def send_Vendor_welcome_email(user_email,first_name,last_name):
    subject = 'Welcome to Roadside'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    html_content = render_to_string('vendor_welcome.html', {'user_email': user_email,"first_name":first_name,"last_name":last_name})

    # Create the email with both plain text and HTML content
    email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
