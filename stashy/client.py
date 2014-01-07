import json
import requests

from .helpers import Nested, add_json_headers
from .admin import Admin
from .projects import Projects
from .compat import basestring


class Stash(object):
    _url = "/"

    def __init__(self, base_url, username, password, verify=True):
        self._client = StashClient(base_url, username, password, verify)

    admin = Nested(Admin)
    projects = Nested(Projects)

    def groups(self, filter=None):
        """
        Consider using stash.admin.groups instead.
        """
        return self.admin.groups.get(filter)

    def users(self, filter=None):
        """
        Consider using stash.admin.users instead.
        """
        return self.admin.users.get(filter)


class StashClient(object):
    api_version = '1.0'

    def __init__(self, base_url, username=None, password=None, verify=True):
        assert isinstance(base_url, basestring)

        self._username = username
        self._password = password
        self._verify=verify

        if base_url.endswith("/"):
            self._base_url = base_url[:-1]
        else:
            self._base_url = base_url

        self._api_base = self._base_url + "/rest/api/" + self.api_version

    def url(self, resource_path):
        assert isinstance(resource_path, basestring)
        if not resource_path.startswith("/"):
            resource_path = "/" + resource_path
        return self._api_base + resource_path

    def head(self, resource, **kw):
        return requests.head(self.url(resource), auth=(self._username, self._password), verify=self._verify, **kw)

    def get(self, resource, **kw):
        return requests.get(self.url(resource), auth=(self._username, self._password), verify=self._verify, **kw)

    def post(self, resource, data=None, **kw):
        if data:
            kw = add_json_headers(kw)
            data = json.dumps(data)
        return requests.post(self.url(resource), data, auth=(self._username, self._password), verify=self._verify, **kw)

    def put(self, resource, data=None, **kw):
        if data:
            kw = add_json_headers(kw)
            data = json.dumps(data)
        return requests.put(self.url(resource), data, auth=(self._username, self._password), verify=self._verify, **kw)

    def delete(self, resource, **kw):
        return requests.delete(self.url(resource), auth=(self._username, self._password), verify=self._verify, **kw)
