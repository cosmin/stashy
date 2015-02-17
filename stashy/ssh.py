# from .helpers import Nested, ResourceBase, IterableResource
from .helpers import ResourceBase, IterableResource
# from .errors import ok_or_error, response_or_error
from .compat import update_doc


class SshFilteredIterableResource(IterableResource):
    def all(self, user=None):
        """
        Retrieve all the resources, optionally modified by filter.
        """
        params = {}
        if user:
            params['user'] = user
        return self.paginate("", params)

    def list(self, user=None):
        """
        Convenience method to return a list (rather than iterable) of all
        elements
        """
        return list(self.all(user))


class Key(ResourceBase):
    def __init__(self, url, client, parent):
        super(Keys, self).__init__(url, client, parent)
        self._url = 'ssh/1.0/keys'

    def get(self):
        return self._client.get(self.url())


class Keys(ResourceBase, SshFilteredIterableResource):
    def __init__(self, url, client, parent):
        super(Keys, self).__init__(url, client, parent)
        self._url = 'ssh/1.0/keys'

    def get(self, user):
        """
        Retrieve the keys matching the supplied user.
        """

        return self._client.get(self.url(user))

    def __getitem__(self, item):
        return Key(item, self.url(item), self._client, self)


update_doc(Keys.all, """Retrieve keys.""")
