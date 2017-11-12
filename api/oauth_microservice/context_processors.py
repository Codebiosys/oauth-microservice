from django.conf import settings


def from_settings(request):
    """ Add various settings properties to the template context.

    Notes
    -----
    - Add more properties here rather than making new contexts.
    """
    return {
        'ENVIRONMENT': settings.ENVIRONMENT,
        'ENVIRONMENT_COLOR': settings.ENVIRONMENT_COLOR,
        'SITENAME': settings.SITENAME,
        'REGISTRATION_OPEN': settings.REGISTRATION_OPEN,
    }
