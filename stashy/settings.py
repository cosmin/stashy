from .errors import response_or_error
from .helpers import Nested, ResourceBase, IterableResource
from .pullrequests import PullRequests


class Hook(ResourceBase):
    def __init__(self, key, url, client, parent):
        super(Hook, self).__init__(url, client, parent)
        self._key = key

    @response_or_error
    def get(self):
        """
        Retrieve a repository hook
        """
        return self._client.get(self.url())

    @response_or_error
    def enable(self, configuration=None):
        """
        Enable a repository hook, optionally applying new configuration.
        """
        return self._client.put(self.url("/enabled"), data=configuration)

    @response_or_error
    def disable(self):
        """
        Disable a repository hook
        """
        return self._client.delete(self.url("/enabled"))

    @response_or_error
    def settings(self):
        """
        Retrieve the settings for a repository hook
        """
        return self._client.get(self.url("/settings"))

    @response_or_error
    def configure(self, configuration):
        """
        Modify the settings for a repository hook
        """
        return self._client.put(self.url("/settings"), data=configuration)


class Hooks(ResourceBase, IterableResource):
    def all(self, type=None):
        """
        Retrieve hooks for this repository, optionally filtered by type.

        type: Valid values are PRE_RECEIVE or POST_RECEIVE
        """
        params = None
        if type is not None:
            params = dict(type=type)
        return self.paginate("", params=params)

    def list(self, type=None):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        return list(self.all(type=type))

    def __getitem__(self, item):
        """
        Return a :class:`Hook` object for operations on a specific hook
        """
        return Hook(item, self.url(item), self._client, self)


class Settings(ResourceBase):
    hooks = Nested(Hooks)
    pullrequests = Nested(PullRequests, relative_path="/pull-requests")
