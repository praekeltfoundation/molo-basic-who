from django.conf import settings
from django.utils.translation import LANGUAGE_SESSION_KEY


def compress_settings(request):
    return {
        'STATIC_URL': settings.STATIC_URL,
        'ENV': settings.ENV,
        'LANGUAGE_CODE': request.session.get(LANGUAGE_SESSION_KEY),
    }
