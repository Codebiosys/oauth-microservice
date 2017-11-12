import datetime

from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from oauth2_provider.models import Application, AccessToken

from .apps import OauthConfig


class OAuthAppTestCase(TestCase):

    def test_settings_loaded_app(self):
        app_name = OauthConfig.name
        self.assertTrue(app_name in settings.INSTALLED_APPS)


class RedirectToAuthorizationViewTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('test_user', 'tester@gmail.com', 'test')

        # Set up OAuth for the user.
        self.application = Application(
            name='Test Application',
            redirect_uris='http://localhost/',
            user=self.test_user,
            skip_authorization=True,
            authorization_grant_type=Application.GRANT_IMPLICIT,
            client_secret='',
            client_type=Application.CLIENT_PUBLIC,
        )
        self.application.save()

        self.valid_token = AccessToken.objects.create(
            user=self.test_user, token='12345678901',
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
        )

    def test_authorize_no_redirect_with_valid_request(self):
        self.client.login(username='test_user', password='test')
        r = self.client.get('/o/authorize/', {
            'client_id': self.application.client_id,
            'response_type': 'token',
        })

        self.assertEqual(r.status_code, 302)
        self.assertNotRegex(r.url, r'http://localhost/\?next=%2F.*')

    def test_authorize_redirect_with_valid_request(self):
        self.client.login(username='test_user', password='test')
        r = self.client.get('/o/authorize/', {
            'next': '/',
            'client_id': self.application.client_id,
            'response_type': 'token',
        })

        self.assertEqual(r.status_code, 302)
        self.assertRegex(r.url, r'http://localhost/\?next=%2F.*')
