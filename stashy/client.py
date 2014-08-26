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

        if base_url.endswith("/"):
            self._base_url = base_url[:-1]
        else:
            self._base_url = base_url

        self._api_base = self._base_url + "/rest/api/" + self.api_version

        self._session = requests.Session()
        self._session.verify = verify
        self._session.cookies = self._session.head(self.url(""), auth=(username, password)).cookies

    def url(self, resource_path):
        assert isinstance(resource_path, basestring)
        if not resource_path.startswith("/"):
            resource_path = "/" + resource_path
        return self._api_base + resource_path

    def head(self, resource, **kw):
        return self._session.head(self.url(resource), **kw)

    def get(self, resource, **kw):
        return self._session.get(self.url(resource), **kw)

    def post(self, resource, data=None, **kw):
        if data:
            kw = add_json_headers(kw)
            data = json.dumps(data)
        return self._session.post(self.url(resource), data, **kw)

    def put(self, resource, data=None, **kw):
        if data:
            kw = add_json_headers(kw)
            data = json.dumps(data)
        return self._session.put(self.url(resource), data, **kw)

    def delete(self, resource, **kw):
        return self._session.delete(self.url(resource), **kw)
