__version__ = "0.1"

from ..helpers import Nested
from .projects import ProjectsExtended
from .admin import Admin
from .client import CoreClient

class Core(object):
    _url = '/'
    def __init__(self, base_url, session):
        self._client = CoreClient(base_url, session=session)
    admin = Nested(Admin)
    projects = Nested(ProjectsExtended, relative_path="/projects")
