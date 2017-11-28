"""
Stashy Build Status Notifications

"""

from enum import Enum

from stashy.helpers import ResourceBase

from stashy.errors import ok_or_error
from stashy.errors import response_or_error


API_NAME = "build-status"
API_VERSION = "1.0"
API_OVERRIDE_PATH = "{api}/{version}/commits".format


class BuildStates(Enum):
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    INPROGRESS = "INPROGRESS"


class Build(ResourceBase):
    def __init__(self, url, client, git_hash):
        super(Build, self).__init__(url, client, None, API_OVERRIDE_PATH(api=API_NAME, version=API_VERSION))
        self._git_hash = git_hash

    def url(self, *args, **kwargs):
        return super(Build, self).url(self._git_hash)

    @ok_or_error
    def set(self, state, key, name, url, description=None):
        """
        Set a build notification for this hash.
           https://developer.atlassian.com/bitbucket/server/docs/latest/how-tos/updating-build-status-for-commits.html
       """
        description = key if description is None else description

        state = BuildStates(state)

        data = {"state": state.value,
                "key": key,
                "name": name,
                "url": url,
                "description": description}

        return self._client.post(self.url(), data=data)

    @response_or_error
    def get(self):
        """
        Get all of the build notifications for this hash
        """
        return self._client.get(self.url())
