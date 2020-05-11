"""
WSGI config for base who.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "who.settings.production")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()