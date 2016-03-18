from .helpers import ResourceBase, Nested, FilteredIterableResource
from .errors import ok_or_error
from .compat import update_doc

class Groups(ResourceBase, FilteredIterableResource):
    def none(self, filter=None):
        """
        Retrieve groups that have no granted permissions.

        filter: return only group names containing the supplied string will be returned
        """
        params = {}
        if filter:
            params['filter'] = filter
        return self.paginate("/none", params)

    @ok_or_error
    def grant(self, group, permission):
        """
        Promote or demote a user's permission level.

        Depending on context, you may use one of the following set of permissions:

        global permissions:

            * LICENSED_USER
            * PROJECT_CREATE
            * ADMIN
            * SYS_ADMIN

        project permissions:
            * PROJECT_READ
            * PROJECT_WRITE
            * PROJECT_ADMIN
        """
        return self._client.put(self.url(), params=dict(name=group, permission=permission))

    @ok_or_error
    def revoke(self, group):
        """
        Revoke all permissions for a group.
        """
        return self._client.delete(self.url(), params=dict(name=group))


class Users(ResourceBase, FilteredIterableResource):
    def none(self, filter=None):
        """
        Retrieve users that have no granted permissions.

        filter: if specified only user names containing the supplied string will be returned
        """
        params = {}
        if filter:
            params['filter'] = filter
        return self.paginate("/none", params)

    @ok_or_error
    def grant(self, user, permission):
        """
        Promote or demote the permission level of a user.


        Depending on context, you may use one of the following set of permissions:

        global permissions:

            * LICENSED_USER
            * PROJECT_CREATE
            * ADMIN
            * SYS_ADMIN

        project permissions:
            * PROJECT_READ
            * PROJECT_WRITE
            * PROJECT_ADMIN

        repository permissions:
            * REPO_READ
            * REPO_WRITE
            * REPO_ADMIN

        """
        return self._client.put(self.url(), params=dict(name=user, permission=permission))

    @ok_or_error
    def revoke(self, user):
        """
        Revoke all permissions for a user.
        """
        return self._client.delete(self.url(), params=dict(name=user))


class Permissions(ResourceBase):
    groups = Nested(Groups)
    users = Nested(Users)


class ProjectPermissions(Permissions):
    def _url_for(self, permission):
        return self.url().rstrip("/") + "/" + permission + "/all"

    @ok_or_error
    def grant(self, permission):
        """
        Grant or revoke a project permission to all users, i.e. set the default permission.

        project permissions:
            * PROJECT_READ
            * PROJECT_WRITE
            * PROJECT_ADMIN

        """
        return self._client.post(self._url_for(permission), params=dict(allow=True))

    @ok_or_error
    def revoke(self, permission):
        """
        Revoke a project permission from all users, i.e. revoke the default permission.

        project permissions:
            * PROJECT_READ
            * PROJECT_WRITE
            * PROJECT_ADMIN

        """
        return self._client.post(self._url_for(permission), params=dict(allow=False))

class RepositoryPermissions(Permissions):
    def _url_for(self):
        return self.url().rstrip("/") + "/users"

    @ok_or_error
    def grant(self, user, permission):
        """
        Grant or revoke a repository permission to all users, i.e. set the
        default permission.

        repository permissions:
            * REPO_READ
            * REPO_WRITE
            * REPO_ADMIN


        """
        return self._client.put(self._url_for(), params=dict(name=user,
                                                              permission=permission))

    @ok_or_error
    def revoke(self, user):
        """
        Revoke a repository permission from all users, i.e. revoke the default
        permission.

        repository permissions:
            * REPO_READ
            * REPO_WRITE
            * REPO_ADMIN

        """
        return self._client.post(self._url_for(), params=dict(name=user))


update_doc(Groups.all, """
Returns groups that have been granted at least one permission.

filter: return only group names containing the supplied string will be returned
""")

update_doc(Users.all, """
Returns users that have been granted at least one permission.

filter: if specified only user names containing the supplied string will be returned
""")
