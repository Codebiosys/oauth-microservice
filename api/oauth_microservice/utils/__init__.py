import yaml


def load_permissions(path):
    """ Returns a list of the permissions listed in
    the provided permissions.yaml file.
    """
    with open(path) as f:
        config = yaml.load(f.read())
    return [
        (key, value)
        for key, value in config['permissions'].items()
    ]


def load_groups(path):
    """ Returns a list of the groups listed in
    the provided permissions.yaml file.
    """
    with open(path) as f:
        config = yaml.load(f.read())
    return [
        (key, value)
        for key, value in config['groups'].items()
    ]


def load_managed_user_groups(path):
    """ Returns a list of the groups listed in
    the provided permissions.yaml file.
    """
    with open(path) as f:
        config = yaml.load(f.read())
    return config['managed_users']['default_groups'] or []


def load_managed_user_permissions(path):
    """ Returns a list of the groups listed in
    the provided permissions.yaml file.
    """
    with open(path) as f:
        config = yaml.load(f.read())
    return config['managed_users']['default_permissions'] or []


def load_sample_users(path):
    """ Returns a list of the user templates listed in
    the provided yaml file.
    """
    with open(path) as f:
        users = yaml.load(f.read())
    return [
        (key, value)
        for key, value in users.items()
    ]
