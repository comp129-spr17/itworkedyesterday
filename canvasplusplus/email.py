'''
* It Worked Yesterday...
* 4/17/17
* canvasplusplus.email.py
* Sets up email system.
'''
from django.core.mail import send_mail

send_mail(
    'Canvas++ Notification',
    'Message here.',
    'canvasplusplus@gmail.com',
    ['to@example.com'],
    fail_silently=False,
)
