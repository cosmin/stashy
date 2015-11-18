__version__ = "0.1"

from .client import Stash

def connect(url, username=None, password=None, verify=True, mutual_authentication=None):
    """Connect to a Stash instance given a username and password.

    This is only recommended via SSL. If you need are using
    self-signed certificates, you can use verify=False to ignore SSL
    verifcation.
    """
    return Stash(url, username, password, verify=verify, mutual_authentication=mutual_authentication)

__all__ = ['connect']
