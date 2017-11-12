import os

from django.core.management import base
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password

from oauth_microservice.utils import load_sample_users


DEFAULT_SAMPLE_USERS_PATH = os.environ.get('SAMPLE_USERS_PATH', 'sample_users.yml')


class Command(base.BaseCommand):
    help = (
        'Remove the built-in permissions and populate the set from the '
        'provided permissions file.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--input',
            help='A YAML file with sample users to create.',
            default=DEFAULT_SAMPLE_USERS_PATH
        )
        parser.add_argument(
            '-f',
            '--force',
            help='Dump all existing users and recreate them.',
            action='store_true',
            default=False
        )

    def log(self, message):
        """ Write log messages to stdout in a consistent format. """
        self.stdout.write('[{date}] {message}'.format(
            date=timezone.now(),
            message=message
        ))

    def handle(self, verbosity, input, force, *args, **kwargs):
        if force:
            self.log(f'Dumping all existing users...')
            User.objects.all().delete()

        for username, details in load_sample_users(input):
            group_names = details.pop('groups')
            password_hash = make_password(details.pop('password'))

            groups = Group.objects.filter(name__in=group_names)

            user_details = {
                **details,
                **{'username': username, 'password': password_hash}
            }

            groups_count = len(groups)
            self.log(f'Creating {username} as a member of {groups_count} groups...')
            user = User.objects.create(**user_details)
            user.groups.set(groups)

        self.log('Done.')
