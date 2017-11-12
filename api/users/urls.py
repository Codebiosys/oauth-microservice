from django.conf.urls import url, include
from rest_framework import routers

import users.views


router = routers.DefaultRouter()
router.register(r'permissions', users.views.UserPermissionsViewSet, base_name='permission')
router.register(r'user', users.views.UserViewSet, base_name='user')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^validate/$', users.views.validate),
    url(r'^user/has_permission/$', users.views.has_permission),
]
