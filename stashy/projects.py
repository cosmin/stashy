from .helpers import Nested, ResourceBase, IterableResource
from .errors import ok_or_error, response_or_error
from .repos import Repos
from .compat import update_doc


class Project(ResourceBase):
    def __init__(self, key, url, client, parent):
        super(Project, self).__init__(url, client, parent)
        self._key = key

    @response_or_error
    def get(self):
        return self._client.get(self.url())

    repos = Nested(Repos)


class Projects(ResourceBase, IterableResource):
    @response_or_error
    def get(self, project):
        """
        Retrieve the project matching the supplied key.
        """
        return self._client.get(self.url(project))

    def __getitem__(self, item):
        return Project(item, self.url(item), self._client, self)


update_doc(Projects.all, """Retrieve projects.""")
