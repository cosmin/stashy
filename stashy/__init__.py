from .core import Core
from .branch_permissions import BranchPermissions
from .client import StashClient

class Stash(object):
    _url = "/"

    def __init__(self, base_url, username=None, password=None, verify=True, session=None):
        self._client = StashClient(base_url, username, password, verify, session=session)

        # init sub-clients
        self.core = Core(base_url, self._client._session)
        self.branch_permissions = BranchPermissions(base_url, self._client._session)


def connect(url, username, password, verify=True):
    """Connect to a Stash instance given a username and password.

    This is only recommended via SSL. If you need are using
    self-signed certificates, you can use verify=False to ignore SSL
    verifcation.
    """
    return Stash(url, username, password, verify)
