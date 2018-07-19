from .helpers import Nested, ResourceBase, IterableResource
from .errors import ok_or_error, response_or_error
from .permissions import Permissions, RepositoryPermissions
from .pullrequests import PullRequests
from .compat import update_doc
from .branch_permissions import BranchPermissions
import json

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
    def all(self, type=None):
        """
        Retrieve hooks for this repository, optionally filtered by type.

        type: Valid values are PRE_RECEIVE or POST_RECEIVE
        """
        params=None
        if type is not None:
            params = dict(type=type)
        return self.paginate("", params=params)

    def list(self, type=None):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        return list(self.all(type=type))

    def __getitem__(self, item):
        """
        Return a :class:`Hook` object for operations on a specific hook
        """
        return Hook(item, self.url(item), self._client, self)

class Webhook(ResourceBase):
    def __init__(self, key, url, client, parent):
        super(Webhook, self).__init__(url, client, parent)
        self._key = key

    @response_or_error
    def get(self):
        """
        Retrieve a repository webhook
        """
        return self._client.get(self.url())

    @response_or_error
    def enable(self, configuration=None):
        """
        Enable a repository webhook, optionally applying new configuration.
        """
        return self._client.put(self.url("/enabled"), data=configuration)

    @response_or_error
    def disable(self):
        """
        Disable a repository webhook
        """
        return self._client.delete(self.url("/enabled"))

    @response_or_error
    def settings(self):
        """
        Retrieve the settings for a repository webhook
        """
        return self._client.get(self.url("/settings"))

    @response_or_error
    def configure(self, configuration):
        """
        Modify the settings for a repository webhook
        """
        return self._client.put(self.url("/settings"), data=configuration)


class Webhooks(ResourceBase, IterableResource):
    def all(self, type=None):
        """
        Retrieve webhooks for this repository, optionally filtered by type.

        type: Valid values are PRE_RECEIVE or POST_RECEIVE
        """
        params=None
        if type is not None:
            params = dict(type=type)
        return self.paginate("", params=params)

    @response_or_error
    def create(self, name, url, events=["repo:refs_changed"], active=True):
        """
        Create a webhook with the given name and url
        """
        return self._client.post(self.url(), data={"name": name,
                                                   "active": active,
                                                   "events": events,
                                                   "url": url
                                                   })

    def list(self, type=None):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        return list(self.all(type=type))

    def __getitem__(self, item):
        """
        Return a :class:`Webhook` object for operations on a specific hook
        """
        return Webhook(item, self.url(item), self._client, self)

class Settings(ResourceBase):
    hooks = Nested(Hooks)
    pullrequests = Nested(PullRequests, relative_path="/pull-requests")


class Repository(ResourceBase):
    def __init__(self, slug, url, client, parent):
        super(Repository, self).__init__(url, client, parent)
        self._slug = slug

    @response_or_error
    def delete(self):
        """
        Schedule the repository to be deleted
        """
        return self._client.delete(self.url())

    @response_or_error
    def update(self, name):
        """
        Update the name of a repository.

        The repository's slug is derived from its name. If the name changes the slug may also change.
        """
        return self._client.post(self.url(), data=dict(name=name))

    @response_or_error
    def get(self):
        """
        Retrieve the repository
        """
        return self._client.get(self.url())

    @response_or_error
    def fork(self, name = None, project = None):
        """
        Fork the repository.

        name    - Specifies the forked repository's name
                    Defaults to the name of the origin repository if not specified
        project - Specifies the forked repository's target project by key
                    Defaults to the current user's personal project if not specified
        
        """
        data = dict()
        if name is not None:
            data['name'] = name
        if project is not None:
            data['project'] = {"key": project}
            
        return self._client.post(self.url(), data=data)

    def forks(self):
        """
        Retrieve repositories which have been forked from this one.
        """
        return self.paginate('/forks')

    @response_or_error
    def tags(self, filterText=None, orderBy=None):
        """
        Retrieve the tags matching the supplied filterText param.
        """
        params = {}
        if filterText is not None:
            params['filterText'] = filterText
        if orderBy is not None:
            params['orderBy'] = orderBy
        return self._client.get(self.url('/tags'), params=params)

    @response_or_error
    def _get_default_branch(self):
        return self._client.get(self.url('/branches/default'))

    @ok_or_error
    def _set_default_branch(self, value):
        return self._client.put(self.url('/branches/default'), data=dict(id=value))

    @ok_or_error
    def create_branch(self, value, origin_branch='master'):
        return self._client.post(self.url('/branches', is_branches=True),
                                data=dict(name=value, startPoint=
                                "refs/heads/%s" % origin_branch))

    @ok_or_error
    def delete_branch(self, value):
        return self._client.delete(self.url('/branches', is_branches=True),
                                data=dict(name=value,
                                          dryRun='false'))
    @response_or_error
    def get_branch_info(self, changesetId):
        return self._client.get(self.url('/branches/info/%s' % changesetId,
                                            is_branches=True))

    def branches(self, filterText=None, orderBy=None, details=None):
        """
        Retrieve the branches matching the supplied filterText param.
        """
        params = {}
        if filterText is not None:
            params['filterText'] = filterText
        if orderBy is not None:
            params['orderBy'] = orderBy
        if details is not None:
            params['details'] = details
        return self.paginate('/branches', params=params)

    default_branch = property(_get_default_branch, _set_default_branch, doc="Get or set the default branch")

    def get_all_branches(self, items):
        """
        Return list of all branches in this project and the repository
        :param items: limit parameter (max items in result)
        :return: 
        """
        branches = self._client.get(self.url('/branches?limit={}'.format(items)))
        return json.loads(branches.content)

    def get_all_tags(self, items):
        """
        Return list of all tags in this project and the repository
        :param items: limit parameter (max items in result)
        :return:
        """
        tags = self._client.get(self.url('/tags?limit={}'.format(items)))
        return json.loads(tags.content)

    def get_commit(self, commit):
        """
        Returns detailed information about a given commit
        :param commit: like "1c972ea39318a4b3ce99bc51ab03277138c586ea"
        :return: 
        """
        res = self._client.get(self.url('/commits/{}'.format(commit)))
        return json.loads(res.content)

    def files(self, path='', at=None):
        """
        Retrieve a page of files from particular directory of a repository. The search is done
        recursively, so all files from any sub-directory of the specified directory will be returned.
        """
        params = {}
        if at is not None:
            params['at'] = at
        return self.paginate('/files/' + path, params)

    def browse(self, path='', at=None, type=False, blame='', noContent=''):
        """
        Retrieve a page of content for a file path at a specified revision.
        """
        params = {}
        if at is not None:
            params['at'] = at
        if type:
            params['type'] = type
            return response_or_error(lambda: self._client.get(self.url('/browse/' + path), params=params))()
        else:
            if blame:
                params['blame'] = blame
            if noContent:
                params['noContent'] = noContent

            return self.paginate("/browse/" + path, params=params, values_key='lines')

    def changes(self, until, since=None):
        """
        Retrieve a page of changes made in a specified commit.

        since: the changeset to which until should be compared to produce a page of changes.
               If not specified the parent of the until changeset is used.

        until: the changeset to retrieve file changes for.
        """
        params = dict(until=until)
        if since is not None:
            params['since'] = since
        return self.paginate('/changes', params=params)

    def commits(self, until, since=None, path=None):
        """
        Retrieve a page of changesets from a given starting commit or between two commits.
        The commits may be identified by hash, branch or tag name.

        since: the changeset id or ref (exclusively) to restrieve changesets after
        until: the changeset id or ref (inclusively) to retrieve changesets before.
        path: an optional path to filter changesets by.

        Support for withCounts is not implement.
        """
        params = dict(until=until, withCounts=False)
        if since is not None:
            params['since'] = since
        if path is not None:
            params['path'] = path
        return self.paginate('/commits', params=params)

    permissions = Nested(Permissions)
    repo_permissions = Nested(RepositoryPermissions,
                              relative_path="/permissions")

    pull_requests = Nested(PullRequests, relative_path="/pull-requests")
    settings = Nested(Settings)
    webhooks = Nested(Webhooks)
    branch_permissions = Nested(BranchPermissions, relative_path=None)


class Repos(ResourceBase, IterableResource):
    @response_or_error
    def create(self, name, scmId="git", forkable=True):
        """
        Create a repository with the given name
        """
        return self._client.post(self.url(), data={"name": name,
                                                   "scmId": scmId,
                                                   "forkable": forkable,
                                                   })

    def __getitem__(self, item):
        """
        Return a :class:`Repository` object for operations on a specific repository
        """
        return Repository(item, self.url(item), self._client, self)


update_doc(Repos.all, """Retrieve repositories from the project""")
