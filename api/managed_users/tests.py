from unittest import mock

from django.test import TestCase


class CreateRemoteUserMixinTestCase(TestCase):

    @mock.patch('django.core.mail.EmailMultiAlternatives.send')
    @mock.patch('django.template.loader.render_to_string')
    def test_send_mail(self, render_to_string, send):
        from managed_users.mixins import CreateRemoteUserMixin

        mixin = CreateRemoteUserMixin()
        mixin.send_mail(
            'test/template',
            'test/template',
            {},
            'test@local',
            'test2@local',
            'test/template'
        )

        self.assertEqual(send.call_count, 1)
        self.assertEqual(render_to_string.call_count, 2)

    @mock.patch('django.core.mail.EmailMultiAlternatives.send')
    @mock.patch('managed_users.mixins.CreateRemoteUserMixin.perform_create')
    @mock.patch('managed_users.mixins.CreateRemoteUserMixin.token_generator.make_token')
    def test_valid_create(self, make_token, perform_create, send):
        from managed_users.mixins import CreateRemoteUserMixin

        mock_user = mock.Mock(
            username='TestUser',
            email='test@local',
            pk=1,
        )

        class CreateRemoteUserMixinView(CreateRemoteUserMixin):
            def get_serializer(self, data=None):
                return mock.Mock(data=mock_user)

        make_token.return_value = 'test-token'
        perform_create.return_value = mock_user
        request = mock.Mock(
            user=mock.Mock(
                has_perm=mock.Mock(return_value=True)
            )
        )

        mixin = CreateRemoteUserMixinView()
        response = mixin.create(request)

        self.assertEqual(send.call_count, 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.username, 'TestUser')
        self.assertEqual(response.data.email, 'test@local')


class ManagedUsersAppTestCase(TestCase):

    def test_settings_loaded_app(self):
        from managed_users.apps import ManagedUsersConfig
        from django.conf import settings

        app_name = ManagedUsersConfig.name
        self.assertTrue(app_name in settings.INSTALLED_APPS)
