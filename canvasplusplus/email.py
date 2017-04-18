from django.core.mail import send_mail

send_mail(
    'Canvas++ Notification',
    'Message here.',
    'canvasplusplus@gmail.com',
    ['to@example.com'],
    fail_silently=False,
)