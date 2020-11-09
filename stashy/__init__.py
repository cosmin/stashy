__version__ = "0.6"

from .client import Stash

def connect(url, username=None, password=None, verify=True, requests_auth=None):
    """Connect to a Stash instance given a username and password.

    This is only recommended via SSL. If you are using self-signed certificates,
    you can use verify=False to ignore SSL verifcation.
    """
    return Stash(url, username, password, verify=verify, requests_auth=requests_auth)

__all__ = ['connect']
