"""
Flickr OAuth support.

This contribution adds support for Flickr OAuth service. The settings
FLICKR_APP_ID and FLICKR_API_SECRET must be defined with the values
given by Flickr application registration process.

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


# Flickr configuration
FLICKR_SERVER = 'http://www.flickr.com/services'
FLICKR_REQUEST_TOKEN_URL = '%s/oauth/request_token' % FLICKR_SERVER
FLICKR_AUTHORIZATION_URL = '%s/oauth/authorize' % FLICKR_SERVER
FLICKR_ACCESS_TOKEN_URL = '%s/oauth/access_token' % FLICKR_SERVER


class FlickrBackend(OAuthBackend):
    """Flickr OAuth authentication backend"""
    name = 'flickr'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('username', 'username'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_details(self, response):
        """Return user details from Flickr account"""
        return {USERNAME: response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}


def get_param(params, val):
    try:
        return params[val][0]
    except (TypeError, KeyError):
        return None
    
class FlickrAuth(ConsumerBasedOAuth):
    """Flickr OAuth authentication mechanism"""
    AUTHORIZATION_URL = FLICKR_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = FLICKR_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = FLICKR_ACCESS_TOKEN_URL
    SERVER_URL = FLICKR_SERVER
    AUTH_BACKEND = FlickrBackend
    SETTINGS_KEY_NAME = 'FLICKR_APP_ID'
    SETTINGS_SECRET_NAME = 'FLICKR_API_SECRET'


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
    'flickr': FlickrAuth,
}
