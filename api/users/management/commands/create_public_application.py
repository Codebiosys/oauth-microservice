import os
import sys

from django.core.management import base
from django.utils import timezone

from oauth2_provider.models import Application
from django.contrib import auth


DEFAULT_CLIENT_ID = os.environ.get('CLIENT_ID', 'a-client-default-key')


class Command(base.BaseCommand):
    help = (
        'Create a simple public, implicit OAuth client application with '
        'the given name and client id.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--name',
            help='The name of the client app that will be created.',
            default='A Client App'
        )

        parser.add_argument(
            '-i',
            '--id',
            help=(
                f'The client id of the client app that will be created. '
                f'You can set the default value of this using the '
                f'environment variable: CLIENT_ID. Seperate multiple ids with ";"'
                f'Default: {DEFAULT_CLIENT_ID}'
            ),
            default=DEFAULT_CLIENT_ID
        )

        parser.add_argument(
            'redirect',
            help='The IP of the client app that will be created. Seperate multiple with ";"'
        )

        parser.add_argument(
            'user',
            help='The user which created the app.'
        )

    def log(self, message):
        """ Write log messages to stdout in a consistent format. """
        date = timezone.now()
        self.stdout.write(f'[{date}] {message}')

    def handle(self, verbosity, user, name, redirect, id, *args, **kwargs):
        try:
            user = auth.models.User.objects.get(username=user)
        except auth.models.User.DoesNotExist:
            self.log(f'No user found with username: {user}')
            return

        self.log('Creating new applications...')

        ids, redirect_uris = id.split(';'), redirect.split(';')
        if len(ids) != len(redirect_uris):
            self.log(
                'Error: Different numbers of ids and redirect_uris given. '
                'Refusing to create applications...'
            )
            sys.exit(-1)

        for client_id, redirect_uri in zip(ids, redirect_uris):
            app = Application.objects.create(
                user=user,
                client_secret='',
                client_type=Application.CLIENT_PUBLIC,
                skip_authorization=True,
                authorization_grant_type=Application.GRANT_IMPLICIT,
                name=name,
                redirect_uris=redirect_uri
            )
            if id is not None:
                app.client_id = client_id
                app.save()
        self.log('Done.')
