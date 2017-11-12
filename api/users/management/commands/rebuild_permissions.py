from django.conf import settings
from django.core.management import base
from django.utils import timezone
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from users.models import PermissionSupport


DELIMETER = '\n- '


class Command(base.BaseCommand):
    help = (
        'Remove the built-in permissions and groups and populate the set '
        'from the provided permissions file.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--force',
            help='Dump all existing groups and permissions and recreate them.',
            action='store_true',
            default=False
        )

    def log(self, message):
        """ Write log messages to stdout in a consistent format. """
        self.stdout.write('[{date}] {message}'.format(
            date=timezone.now(),
            message=message
        ))

    def handle_permissions(self, permissions):
        content_type = ContentType.objects.get_for_model(PermissionSupport)

        # Load the permissions from the global permissions file.
        for codename, description in permissions:
            qs = Permission.objects.filter(codename=codename)
            if not qs.exists():
                self.log(f'Creating permission: {codename}...')
                Permission.objects.create(
                    codename=codename,
                    name=description,
                    content_type=content_type
                )
            else:
                self.log(f'Permission {codename} already exists. Skipping...')

    def handle_groups(self, groups):
        for name, permissions in groups:
            qs = Group.objects.filter(name=name)

            # Create Group
            if not qs.exists():
                self.log(f'Creating group: "{name}"...')
                group = Group.objects.create(name=name)
            else:
                self.log(f'Group "{name}" already exists. Skipping...')
                group = qs.first()

            # Add Permissions to group
            group_name = f'Group: {name}'
            joined_permissions = DELIMETER + DELIMETER.join(permissions)
            line = '-' * len(group_name)
            self.log(
                f'Setting permissions for group:\n\n{group_name}\n'
                f'{line}{joined_permissions}\n\n'
            )
            group.permissions.set(
                Permission.objects.filter(codename__in=permissions)
            )

    def handle(self, verbosity, force=False, *args, **kwargs):
        if force:
            self.log('Dropping existing groups and permissions...')
            Permission.objects.all().delete()
            Group.objects.all().delete()

        self.handle_permissions(settings.DEFAULT_PERMISSIONS)
        self.handle_groups(settings.DEFAULT_GROUPS)

        self.log('Done.')
