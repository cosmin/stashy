__version__ = "0.1"

from ..helpers import Nested
from .client import BranchPermissionsClient
from .projects import ProjectsBranchPermissions

class BranchPermissions(object):
    _url = '/'
    def __init__(self, base_url, session):
        self._client = BranchPermissionsClient(base_url, session=session)

    projects = Nested(ProjectsBranchPermissions, relative_path='/projects')
