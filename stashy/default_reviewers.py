from .helpers import ResourceBase, IterableResource, Nested
from .errors import ok_or_error, response_or_error
from .compat import update_doc

API_NAME = 'default-reviewers'
API_VERSION = '1.0'
API_OVERRIDE_PATH = '{0}/{1}'.format(API_NAME, API_VERSION)

class Condition(ResourceBase):
    def __init__(self, id, url, client, parent):
        super(Condition, self).__init__(url, client, parent, API_OVERRIDE_PATH)
        self._id = id

    @response_or_error
    def get(self):
        """
        Retrieve a condition
        """
        return self._client.get(self.url())


class Conditions(ResourceBase):

    def __init__(self, url, client, parent):
        ResourceBase.__init__(self, url, client, parent, API_OVERRIDE_PATH)

    def __getitem__(self, item):
        return Condition(item, self.url(str(item)), self._client, self)

    def __iter__(self):
        return iter(self.list())

    @response_or_error
    def list(self):
        return self._client.get(self.url())


class DefaultReviewers(ResourceBase):
    """Simple parent resource for this api, to distinguish conditions from anything else"""
    conditions = Nested(Conditions)
