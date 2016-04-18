# from .helpers import Nested, ResourceBase, IterableResource
from .helpers import ResourceBase, IterableResource
from .errors import ok_or_error, response_or_error
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

    @ok_or_error
    def create(self, user, key, label=None):
        """
        Adds the key for the supplied user. If label is not set then
        the comment part of the key is used as it.
        """
        data = dict(text=key, label=label)
        params = dict(user=user)
        return self._client.post(self.url(""), data=data, params=params)

    @response_or_error
    def get(self, user):
        """
        Retrieve the keys matching the supplied user.
        """
        params = dict(user=user)
        return self._client.get(self.url(""), params=params)

    def __getitem__(self, item):
        return Key(item, self.url(item), self._client, self)


update_doc(Keys.all, """Retrieve keys.""")
