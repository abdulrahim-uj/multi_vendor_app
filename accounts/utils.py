from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def detect_user(user):
    if user.role == 1:
        redirect_url = "accounts:vendorControlPanel"
        return redirect_url
    elif user.role == 2:
        redirect_url = "accounts:userControlPanel"
        return redirect_url
    elif user.role is None and user.is_superadmin:
        redirect_url = "/admin"
        return redirect_url


def send_verification_email(request, user, mail_subject, mail_template):
    current_site = get_current_site(request)
    message_body = render_to_string(mail_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(subject=mail_subject, body=message_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[to_email])
    mail.send()


def send_notification_email(mail_subject, mail_template, context):
    message_body = render_to_string(mail_template, context)
    to_email = context['user'].email
    mail = EmailMessage(subject=mail_subject, body=message_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[to_email])
    mail.send()
