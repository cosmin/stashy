from .helpers import Nested, ResourceBase, IterableResource
from .permissions import ProjectPermissions
from .errors import ok_or_error, response_or_error
from .repos import Repos
from .compat import update_doc


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

    permissions = Nested(ProjectPermissions, relative_path="/permissions")
    repos = Nested(Repos)


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
