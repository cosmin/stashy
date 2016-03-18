from .helpers import ResourceBase, IterableResource
from .repos import Repository
from .compat import update_doc

class Repos(ResourceBase, IterableResource):
  def __getitem__(self, item):
    """
    Return a :class:`Repository` object for operations on a specific repository
    """
    return Repository(item, self.url(item), self._client, self)

update_doc(Repos.all, """Retreive repositories from Stash""")
