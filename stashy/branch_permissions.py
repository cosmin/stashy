from .helpers import ResourceBase, IterableResource, Nested
from .errors import ok_or_error, response_or_error
from .compat import update_doc

API_NAME = 'branch-permissions'
API_VERSION = '1.0'
API_OVERRIDE_PATH = '{0}/{1}'.format(API_NAME, API_VERSION)

class Permitted(ResourceBase, IterableResource):
    """Get-only resource that describes a permission record"""
    def __init__(self, url, client, parent):
        ResourceBase.__init__(self, url, client, parent, API_OVERRIDE_PATH)

update_doc(Permitted.all, """Retrieve list of permitted entities for a repo""")


class Restriction(ResourceBase):
    def __init__(self, id, url, client, parent):
        super(Restriction, self).__init__(url, client, parent, API_OVERRIDE_PATH)
        self._id = id

    @response_or_error
    def get(self):
        """
        Retrieve a restriction
        """
        return self._client.get(self.url())

    @ok_or_error
    def delete(self):
        """
        Delete a restriction
        """
        return self._client.delete(self.url())

    @response_or_error
    def update(self, value, users=None, groups=None, pattern=False):
        """
        Re-restrict a branch, or set of branches defined by a pattern, to a set of users and/or groups
        """
        data = dict(type=('PATTERN' if pattern else 'BRANCH'), value=value)

        if users is not None:
            data['users'] = users
        if groups is not None:
            data['groups'] = groups

        return self._client.put(self.url(""), data=data)


class Restricted(ResourceBase, IterableResource):

    def __init__(self, url, client, parent):
        ResourceBase.__init__(self, url, client, parent, API_OVERRIDE_PATH)

    def __getitem__(self, item):
        return Restriction(item, self.url(item), self._client, self)

    @response_or_error
    def create(self, value, users=None, groups=None, pattern=False):
        """
        Restrict a branch, or set of branches defined by a pattern, to a set of users and/or groups
        """
        data = dict(type=('PATTERN' if pattern else 'BRANCH'), value=value)

        if users is not None:
            data['users'] = users
        if groups is not None:
            data['groups'] = groups

        return self._client.post(self.url(""), data=data)

update_doc(Restricted.all, """Retrieve list of restrictions for a repo""")

class BranchPermissions(ResourceBase):
    """Simple parent resource for this api, to distinguish permissions from permitted"""
    permitted = Nested(Permitted)
    restricted = Nested(Restricted)
