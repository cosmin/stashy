from .branch_permissions import BranchPermissions
from .default_reviewers import DefaultReviewers
from .compat import update_doc
from .errors import ok_or_error, response_or_error
from .helpers import Nested, ResourceBase, IterableResource
from .permissions import ProjectPermissions
from .repos import Repos
from .settings import Settings

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
    def all(self, type=None, params = None):
        """
        Retrieve hooks for this repository, optionally filtered by type.

        type: Valid values are PRE_RECEIVE or POST_RECEIVE
        """
        if params is None: params = dict()
        
        # the below condition is to just ensure the params doesnt contain type.
        if type is not None and type not in params: params.update(dict(type=type))
        return self.paginate("", params=params)

    def list(self, type=None, params = None):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        if params is None: params = dict()
        
        # the below condition is to just ensure the params doesnt contain type.
        if type is not None and type not in params: params.update(dict(type=type))
        return list(self.all(type=type))

    def __getitem__(self, item):
        """
        Return a :class:`Hook` object for operations on a specific hook
        """
        return Hook(item, self.url(item), self._client, self)


class Settings(ResourceBase):
    hooks = Nested(Hooks)

class Project(ResourceBase):
    def __init__(self, key, url, client, parent):
        super(Project, self).__init__(url, client, parent)
        self._key = key

    @ok_or_error
    def delete(self):
        """
        Delete the project
        """
        return self._client.delete(self.url())

    @response_or_error
    def update(self, new_key=None, name=None, description=None, avatar=None, public=None):
        """
        Update project information. If supplied, avatar should be a base64 encoded image.

        None is used as a sentinel so use '' to clear a value.
        """
        data = dict()
        if new_key is not None:
            data['key'] = new_key
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        if avatar is not None:
            data['avatar'] = "data:image/png;base64," + avatar
        if public is not None:
            data['public'] = public

        return self._client.put(self.url(), data)

    @response_or_error
    def get(self):
        return self._client.get(self.url())

    def keys(self):
        """
        Retrieve the access keys associated with the project
        """
        return self.paginate('/ssh', is_keys=True)

    @ok_or_error
    def add_key(self, key_text, permission):
        return self._client.post(self.url('/ssh', is_keys=True),
                                 data=dict(key=dict(text=key_text),
                                           permission=permission))


    permissions = Nested(ProjectPermissions, relative_path="/permissions")
    repos = Nested(Repos)
    settings = Nested(Settings)
    branch_permissions = Nested(BranchPermissions, relative_path=None)
    default_reviewers = Nested(DefaultReviewers, relative_path=None)


class Projects(ResourceBase, IterableResource):
    @response_or_error
    def get(self, project):
        """
        Retrieve the project matching the supplied key.
        """
        return self._client.get(self.url(project))

    def __getitem__(self, item):
        return Project(item, self.url(item), self._client, self)

    @response_or_error
    def create(self, key, name, description='', avatar=None):
        """
        Create a project. If supplied, avatar should be a base64 encoded image.
        """
        data = dict(key=key, name=name, description=description)
        if avatar:
            data['avatar'] = "data:image/png;base64," + avatar
        return self._client.post(self.url(), data)


update_doc(Projects.all, """Retrieve projects.""")
