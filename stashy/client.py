import json
import requests

from .core.helpers import Nested, add_json_headers
from .core.admin import Admin
from .core.projects import Projects
from .core.compat import basestring


class StashClient(object):
    api_version = '1.0'

    def __init__(self, base_url, username=None, password=None, verify=True, session=None):
        assert isinstance(base_url, basestring)

        if base_url.endswith("/"):
            self._base_url = base_url[:-1]
        else:
            self._base_url = base_url

        # this won't be functional without being subclassed
        self._api_base = self._base_url

        if session is None:
            session = requests.Session()

        self._session = session
        self._session.verify = verify

        if username is not None or password is not None:
            self._session.auth = (username, password)

        self._session.cookies = self._session.head(self.url("")).cookies

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
