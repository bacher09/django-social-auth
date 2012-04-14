"""
Fitbit OAuth support.

This contribution adds support for Fitbit OAuth service. The settings
FITBIT_CONSUMER_KEY and FITBIT_CONSUMER_SECRET must be defined with the values
given by Fitbit application registration process.

By default account id, username and token expiration time are stored in
extra_data field, check OAuthBackend class for details on how to extend it.
"""
try:
    from urlparse import parse_qs
    parse_qs  # placate pyflakes
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs

from oauth2 import Token

from social_auth.utils import setting
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME
from social_auth.backends.flickr import get_param


# Fitbit configuration
FITBIT_SERVER = 'https://api.fitbit.com'
FITBIT_REQUEST_TOKEN_URL = '%s/oauth/request_token' % FITBIT_SERVER
FITBIT_AUTHORIZATION_URL = '%s/oauth/authorize' % FITBIT_SERVER
FITBIT_ACCESS_TOKEN_URL = '%s/oauth/access_token' % FITBIT_SERVER
EXPIRES_NAME = setting('SOCIAL_AUTH_EXPIRATION', 'expires')


class FitbitBackend(OAuthBackend):
    """Fitbit OAuth authentication backend"""
    name = 'fitbit'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'),
                  ('username', 'username'),
                  ('expires', EXPIRES_NAME)]

    def get_user_details(self, response):
        """Return user details from Fitbit account"""
        return {USERNAME: response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}


class FitbitAuth(ConsumerBasedOAuth):
    """Fitbit OAuth authentication mechanism"""
    AUTHORIZATION_URL = FITBIT_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = FITBIT_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = FITBIT_ACCESS_TOKEN_URL
    SERVER_URL = FITBIT_SERVER
    AUTH_BACKEND = FitbitBackend
    SETTINGS_KEY_NAME = 'FITBIT_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'FITBIT_CONSUMER_SECRET'
    
    
    def user_data(self, access_token, response, *args, **kwargs):
        """Loads user data from service"""
        params = parse_qs(response)
        return {
            'id': get_param(params, 'user_nsid'),
            'username': get_param(params, 'fullname'),
            'fullname': get_param(params, 'username'),
        }


# Backend definition
BACKENDS = {
    'fitbit': FitbitAuth,
}
