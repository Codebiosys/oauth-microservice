from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^authorize/$', views.RedirectToAuthorizationView.as_view()),
    url(r'^', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
