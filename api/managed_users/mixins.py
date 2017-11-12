from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin


managed_user_settings = settings.REMOTE_USER_MANAGEMENT


class CreateRemoteUserMixin(CreateModelMixin):
    """ Allow a remote user to be created with default permissions if the
    requesting user has permission to do so.

    Creating a Remote User does not allow for the setting of a password.
    The new user is required to set their first time password.

    This mixin will provide all of the functionality for managing managed users.
    """
    managing_user_permission = managed_user_settings['MANAGING_USER_PERMISSION']

    subject_template_name = 'managed_users/welcome_password_reset_subject.txt'
    email_template_name = 'managed_users/welcome_password_reset_email.html'
    token_generator = default_token_generator
    from_email = settings.DEFAULT_FROM_EMAIL
    use_https = settings.USE_SSL

    PERMISSION_DENIED_MESSAGE = 'You do not have permission to create managed users.'

    def get_password_reset_email_context(self, user, request):
        current_site = get_current_site(request)
        return {
            'email': user.email,
            'domain': current_site.domain,
            'site_name': current_site.name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'user': user,
            'token': self.token_generator.make_token(user),
            'protocol': 'https' if self.use_https else 'http',
        }

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.send()

    def create(self, request, *args, **kwargs):
        """ Create the user given in the request.

        If the requesting user has sufficient management permissions, create
        the requested user and send them an email informing them that they've
        been added to the system and that they need to reset their password
        to gain access.

        Validation and Permission errors are raised to leverage DRF's built-in
        exception handling and response formats.
        """
        # Validate that the requesting user is allowed to create managed users
        if not request.user.has_perm(self.managing_user_permission):
            raise PermissionDenied(self.PERMISSION_DENIED_MESSAGE)

        # Create the new managed user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # Send new user a password reset email
        context = self.get_password_reset_email_context(user, request)
        self.send_mail(
            self.subject_template_name,
            self.email_template_name,
            context,
            self.from_email,
            user.email,
        )

        # Let the requesting user know that a new user was successfully created
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
