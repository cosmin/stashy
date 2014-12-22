from ..helpers import Nested
from .repos import ReposBranchPermissions
from ..compat import update_doc
from ..projects import Project, Projects


class ProjectBranchPermissions(Project):
    def __init__(self, key, url, client, parent):
        super(ProjectBranchPermissions, self).__init__(key, url, client, parent)

    repos = Nested(ReposBranchPermissions, relative_path='/repos')


class ProjectsBranchPermissions(Projects):

    def __getitem__(self, item):
        return ProjectBranchPermissions(item, self.url(item), self._client, self)


update_doc(ProjectsBranchPermissions.all, """Retrieve projects.""")
