from .helpers import ResourceBase, IterableResource, Nested
from .errors import ok_or_error, response_or_error
from .compat import update_doc

from enum import Enum

API_NAME = 'branch-permissions'
API_VERSION = '2.0'
API_OVERRIDE_PATH = '{0}/{1}'.format(API_NAME, API_VERSION)


class Matcher(Enum):
    """Valid values for the matcher_type for Restriction create/update"""
    PATTERN = 'PATTERN'
    BRANCH = 'BRANCH'
    MODEL_CATEGORY = 'MODEL_CATEGORY'
    MODEL_BRANCH = 'MODEL_BRANCH'


class RestrictionType(Enum):
    """Valid values for the restriction_type for Restriction create/update"""
    PULL_REQUEST = 'pull-request-only'
    FAST_FORWARD = 'fast-forward-only'
    NO_DELETES = 'no-deletes'
    READ_ONLY = 'read-only'


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

    @staticmethod
    def request_data(match, users, groups, keys, restriction_type,
                     matcher_type):
        data = dict(type=restriction_type.value)
        data['matcher'] = dict(type={'id': matcher_type.value}, id=match)

        if users is not None:
            data['users'] = users
        if groups is not None:
            data['groups'] = groups
        if keys is not None:
            data['accessKeys'] = keys

        return data

    @response_or_error
    def update(self, match, users=None, groups=None, keys=None,
               restriction_type=RestrictionType.READ_ONLY,
               matcher_type=Matcher.PATTERN):
        """
        Re-restrict a branch, or set of branches defined by a pattern,
        to a set of users, groups, and access keys.
        Warning: The REST API does not actually support a direct update of
        branch permissions. The Restriction will be deleted and recreated instead.
        Note: access keys need to be specified by their numerical id. labels are
        not accepted.
        """
        data = self.request_data(match, users, groups, keys, restriction_type,
                                 matcher_type)
        self.delete()
        return self._client.post(self._parent.url(), data=data)


class Restrictions(ResourceBase, IterableResource):

    def __init__(self, url, client, parent):
        ResourceBase.__init__(self, url, client, parent, API_OVERRIDE_PATH)

    def __getitem__(self, item):
        return Restriction(item, self.url(item), self._client, self)

    @response_or_error
    def create(self, match, users=None, groups=None, keys=None,
               restriction_type=RestrictionType.READ_ONLY,
               matcher_type=Matcher.PATTERN):
        """
        Restrict a branch, or set of branches defined by a pattern,
        to a set of users, groups, and access keys.
        Note: access keys need to be specified by their numerical id. labels are
        not accepted.
        """
        data = Restriction.request_data(match, users, groups, keys,
                                        restriction_type, matcher_type)

        return self._client.post(self.url(""), data=data)


update_doc(Restrictions.all, """Retrieve list of restrictions for a repo""")


class BranchPermissions(ResourceBase):
    """Simple parent resource for this api, to distinguish restrictions from anything else"""
    restrictions = Nested(Restrictions)
