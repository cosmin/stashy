from ..helpers import Nested
from .permissions import ProjectPermissions
from ..errors import ok_or_error, response_or_error
from .repos import ReposCore
from ..compat import update_doc
from ..projects import Project, Projects


class ProjectCore(Project):
    def __init__(self, key, url, client, parent):
        super(ProjectCore, self).__init__(key, url, client, parent)

    @ok_or_error
    def delete(self):
        """
        Delete the project
        """
        return self._client.delete(self.url())

    @response_or_error
    def update(self, project, new_key=None, name=None, description=None, avatar=None):
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

        return self._client.post(self.url(), data)

    permissions = Nested(ProjectPermissions, relative_path="/permissions")
    repos = Nested(ReposCore, relative_path='/repos')


class ProjectsCore(Projects):

    def __getitem__(self, item):
        return ProjectCore(item, self.url(item), self._client, self)

    @response_or_error
    def create(self, key, name, description='', avatar=None):
        """
        Create a project. If supplied, avatar should be a base64 encoded image.
        """
        data = dict(key=key, name=name, description=description)
        if avatar:
            data['avatar'] = "data:image/png;base64," + avatar
        return self._client.post(self.url(), data)


update_doc(ProjectsCore.all, """Retrieve projects.""")
