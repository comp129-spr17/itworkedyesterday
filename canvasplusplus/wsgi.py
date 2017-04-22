"""
WSGI config for canvasplusplus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
'''
* It Worked Yesterday...
* 3/20/17
* canvasplusplus.wsgi.py
* Auto-generated Django file.
'''
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "canvasplusplus.settings")

application = get_wsgi_application()
