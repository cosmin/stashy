from ..helpers import Nested
from ..errors import response_or_error
from .branch_permissions import Permitted
from ..compat import update_doc
from ..repos import Repository, Repos


class RepositoryBranchPermissions(Repository):
    def __init__(self, slug, url, client, parent):
        super(RepositoryBranchPermissions, self).__init__(slug, url, client, parent)

    permitted = Nested(Permitted)


class ReposBranchPermissions(Repos):
    @response_or_error
    def create(self, name, scmId="git", forkable=True):
        """
        Create a repository with the given name
        """
        return self._client.post(self.url(), data={"name": name,
                                                   "scmId": scmId,
                                                   "forkable": forkable,
                                                   })

    def __getitem__(self, item):
        """
        Return a :class:`Repository` object for operations on a specific repository
        """
        return RepositoryBranchPermissions(item, self.url(item), self._client, self)


update_doc(ReposBranchPermissions.all, """Retrieve repositories from the project""")
