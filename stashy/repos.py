from .helpers import ResourceBase, IterableResource
from .errors import response_or_error
from .compat import update_doc


class Repository(ResourceBase):
    def __init__(self, slug, url, client, parent):
        super(Repository, self).__init__(url, client, parent)
        self._slug = slug

    @response_or_error
    def get(self):
        """
        Retrieve the repository
        """
        return self._client.get(self.url())


class Repos(ResourceBase, IterableResource):

    def __getitem__(self, item):
        """
        Return a :class:`Repository` object for operations on a specific repository
        """
        return Repository(item, self.url(item), self._client, self)


update_doc(Repos.all, """Retrieve repositories from the project""")
