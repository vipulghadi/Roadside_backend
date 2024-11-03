from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_html_email(user_email):
    subject = 'Welcome to Our Service'
    html_message = render_to_string('welcome_email_template.html', {'user': 'John'})
    from_email = 'your_email@gmail.com'
    recipient_list = [user_email]

    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.content_subtype = 'html' 
    email.send()
