# from django.conf import settings
# from django.core.mail import send_mail



# def send_account_activation_email(email,email_token):
#     subject = 'Your account needs to be verified'
#     email_from = settings.EMAIL_HOST_USER
#     message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
# activation_url = f"http://{settings.HOST_NAME}/accounts/activate/{email_token}/"
#     send_mail(subject, message, email_from, [email])

# from django.conf import settings
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags


# def send_account_activation_email(email, email_token):
#     subject = 'Your account needs to be verified'
#     email_from = settings.EMAIL_HOST_USER
#     template = 'email/activation_email.html'
#     context = {'email_token': email_token}
#     message = render_to_string(template, context)
#     plain_message = strip_tags(message)

#     send_mail(subject, plain_message, email_from, [email], html_message=message)

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_account_activation_email(email, email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    activation_url = f'http://127.0.0.1:8000/accounts/activate/{email_token}/'
    context = {'activation_url': activation_url}

    message = render_to_string('email/activation_email.html', context)
    plain_message = strip_tags(message)

    send_mail(subject, plain_message, email_from, [email], html_message=message)

