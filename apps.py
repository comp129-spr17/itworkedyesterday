from django_safari_notifications.apps import DjangoSafariNotificationsConfig
from django.apps import AppConfig


class CanvasPlusPlusConfig(AppConfig):
    name = 'canvasplusplus'


class MySafariNotificationsConfig(DjangoSafariNotificationsConfig):
    cert = '/path/to/cert.pem'
    passphrase = 'passphrase for key'
