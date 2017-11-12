from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from rest_framework.documentation import include_docs_urls
from registration import views


if settings.ENABLE_REMOTE_USER_MANAGEMENT:
    managed_users_urls = (url(r'^', include('managed_users.urls')),)
else:
    managed_users_urls = []


urlpatterns = (
    # API
    url(r'^', include('users.urls')),
    *managed_users_urls,

    # Django-Registration and django.contrib.auth URLs
    # Instead of using the built-in includes from django-registration, we manually
    # include the views here. This is because of a bug in the auto-included
    # auth views in django-registration v2.4, so we recreate all of the URLs here.
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^register/$',
        views.RegistrationView.as_view(),
        name='registration_register'),
    url(r'^register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'
        ),
        name='registration_disallowed'),

    # TODO: Remove base login since nothing needs it.
    # We only need token and console admin logins.

    # OAuth Override Views
    url(r'^o/', include('oauth.urls')),

    # Django Admin Panel
    url(r'^console/', admin.site.urls),

    # Schema and Docs
    url(r'^docs/', include_docs_urls(title='OAuth Microservice'))
)

# Name the admin site.
admin.site.site_header = '{} Admin Panel'.format(settings.SITENAME)
admin.site.site_title = admin.site.site_header
