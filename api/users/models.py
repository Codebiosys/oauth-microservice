from django.db import models


class PermissionSupport(models.Model):
    """ A support model that removes the permissions coupling
    from any existing models since the OAuth Provider doesn't
    have any models from the actual project.

    Source:
    https://stackoverflow.com/a/37988537/2085172

    Notes
    -----

    Django's Permission Model is pretty simple and has the following
    important fields:

    - id: The table's primary key.
    - codename: A programmer-friendly unique id which summarizes the permission.
    - name: A display name describing the permission. Suitable for showing in a user interface.
    """
    class Meta:
        # No database table creation or deletion operations \
        # will be performed for this model.
        managed = False
