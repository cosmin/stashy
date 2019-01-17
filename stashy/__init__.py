__version__ = "0.6"

from .client import Stash

def connect(url, username, password, verify=True):
    """Connect to a Stash instance given a username and password.

    This is only recommended via SSL. If you need are using
    self-signed certificates, you can use verify=False to ignore SSL
    verifcation.
    """
    return Stash(url, username, password, verify=verify)

__all__ = ['connect']
