from django.conf.urls import url, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'managed_users', views.ManagedUserViewSet, base_name='managed_users')

urlpatterns = [
    url(r'^', include(router.urls)),
]
