from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from oauth2_provider.views import AuthorizationView


class RedirectToAuthorizationView(AuthorizationView):
    """ A subclass of OAuth Toolkit's default AuthorizationView which allows the
    client to specify a `redirect_to` URL param that is forwarded to the client
    upon successful authorization.
    """

    REDIRECT_PARAM = settings.OAUTH_REDIRECT_PARAM

    def get(self, request, *args, **kwargs):
        """ During get requests for the types of authorization requests that
        the OAuth Provider AuthorizationView handles:

        * Authorization code
        * Implicit grant

        allow the client to supply a `redirect_to` URL Param which will be
        forwarded to the client after the authorization completes successfully.
        """
        # Extract the optional `redirect_to` URL param and saves it for later.
        redirect_to = request.GET.get(self.REDIRECT_PARAM, None)

        # Perform OAuth Toolkit's default auth behavior.
        response = super().get(request, *args, **kwargs)

        # Check if the response is a `HttpResponseRedirect` and if it is
        # then reconstruct the response and add the redirect to the response.
        # Also do nothing if we weren't given a `redirect_to` param.
        # Otherwise just do what OAuth Toolkit would normally do.
        if not isinstance(response, HttpResponseRedirect) or not redirect_to:
            return response

        # Add the query param to the existing URL.
        scheme, netloc, path, params, query, fragment = urlparse(response.url)
        new_query = urlencode({
            **parse_qs(query),
            self.REDIRECT_PARAM: redirect_to
        })
        new_url = urlunparse((scheme, netloc, path, params, new_query, fragment))

        return redirect(new_url)
