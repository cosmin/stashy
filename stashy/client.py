import json
import requests

from .helpers import Nested, add_json_headers
from .admin import Admin
from .projects import Projects
from .ssh import Keys
from .compat import basestring
from .allrepos import Repos
from .builds import Build

class Stash(object):
    _url = "/"

    def __init__(self, base_url, username=None, password=None, oauth=None, verify=True, token=None, session=None):
        self._client = StashClient(base_url, username, password, oauth, verify, token, session=session)

    admin = Nested(Admin)
    projects = Nested(Projects)
    ssh = Nested(Keys)
    repos = Nested(Repos)

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

    def build(self, git_hash):
        """
        Get build information for a commit.
        """
        return Build("", self._client, git_hash)


class StashClient(object):

    # the core api path will be used as an overridable default
    core_api_name = 'api'
    core_api_version = '1.0'
    core_api_path = '{0}/{1}'.format(core_api_name, core_api_version)

    branches_api_name = 'branch-utils'
    branches_api_version = '1.0'
    branches_api_path = '{0}/{1}'.format(branches_api_name, branches_api_version)

    git_api_name = 'git'
    git_api_version = '1.0'
    git_api_path = '{0}/{1}'.format(git_api_name, git_api_version)

    sync_api_name = 'sync'
    sync_api_version = 'latest'
    sync_api_path = '{0}/{1}'.format(sync_api_name, sync_api_version)

    def __init__(self, base_url, username=None, password=None, oauth=None, verify=True, token=None, session=None):
        assert isinstance(base_url, basestring)

        if base_url.endswith("/"):
            self._base_url = base_url[:-1]
        else:
            self._base_url = base_url

        self._api_base = self._base_url + "/rest"

        if session is None:
            session = requests.Session()

        self._session = session
        self._session.verify = verify

        if oauth is not None:
            self._create_oauth_session(oauth)
        elif username is not None or password is not None:
            self._session.auth = (username, password)
        elif token is not None:
            self._session.headers.update({'Authorization': 'Bearer {}'.format(token)})

        self._session.cookies = self._session.head(self.url("")).cookies
        self._session.headers.update({'Content-Type': 'application/json'})

    def _create_oauth_session(self, oauth):
        from requests_oauthlib import OAuth1
        from oauthlib.oauth1 import SIGNATURE_RSA

        oauth = OAuth1(
            oauth['consumer_key'],
            rsa_key=oauth['key_cert'],
            signature_method=SIGNATURE_RSA,
            resource_owner_key=oauth['access_token'],
            resource_owner_secret=oauth['access_token_secret']
        )
        self._session.auth = oauth

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

    def delete(self, resource, data=None,**kw):
        if data:
            data = json.dumps(data)
            kw = add_json_headers(kw)
            return self._session.request(method='DELETE', url=self.url(
                resource), data=data, **kw)
        return self._session.delete(self.url(resource), **kw)
