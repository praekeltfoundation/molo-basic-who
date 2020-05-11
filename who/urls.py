import os

from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django_cas_ng import views as cas_views
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from who.views import health_who


if settings.ENABLE_SSO:
    urlpatterns = [
        path(r'^admin/login/',
            cas_views.LoginView.as_view(), name='cas_ng_login'),
        path(r'^admin/logout/',
            cas_views.LogoutView.as_view(), name='cas_ng_logout'),
        path(r'^admin/callback/',
            cas_views.CallbackView.as_view(), name='cas_ng_callback'),
    ]
else:
    urlpatterns = []

urlpatterns += [
    path(r'^django-admin/', admin.site.urls),
    path(r'^admin/', include(wagtailadmin_urls)),
    path(r'^documents/', include(wagtaildocs_urls)),
    path(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    path(r'^sitemap\.xml$', sitemap),
    path(r'^health/$', health_who, name='health_who'),
    path(r'', include('molo.core.urls')),
    path(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + 'images/',
        document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
