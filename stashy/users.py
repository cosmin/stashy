from .compat import update_doc
from .errors import ok_or_error, response_or_error
from .helpers import Nested, ResourceBase, IterableResource
from .repos import Repos


class User(ResourceBase):
    def __init__(self, key, url, client, parent):
        super(User, self).__init__(url, client, parent)
        self._key = key

    @response_or_error
    def get(self):
        return self._client.get(self.url())

    repos = Nested(Repos)


class Users(ResourceBase, IterableResource):
    @response_or_error
    def get(self, user):
        """
        Retrieve the user matching the supplied key.
        """
        return self._client.get(self.url(user))

    def __getitem__(self, item):
        return User(item, self.url(item), self._client, self)


update_doc(Users.all, """Retrieve Users.""")
