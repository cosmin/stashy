from .helpers import Nested, ResourceBase, IterableResource
from .errors import ok_or_error, response_or_error


class PullRequestRef(object):
    def __init__(self, project_key, repo_slug, id):
        self.project_key = project_key
        self.repo_slug = repo_slug
        self.id = id

    def to_dict(self):
        return dict(id=self.id,
                    repository=dict(slug=self.repo_slug,
                                    project=dict(key=self.project_key),
                                    name=self.repo_slug))


class PullRequest(ResourceBase):
    def __init__(self, id, url, client, parent):
        super(PullRequest, self).__init__(url, client, parent)
        self._id = id

    @response_or_error
    def get(self):
        """
        Retrieve a pull request.
        """
        return self._client.get(self.url())


    @response_or_error
    def update(self, version, title=None, description=None, reviewers=None):
        """
        Update the title, description or reviewers of an existing pull request.

        Note: the reviewers list may be updated using this resource. However the author and participants list may not.
        """
        data = dict(id=self._id, version=version)
        if title is not None:
            data['title'] = title
        if description is not None:
            data['description'] = description
        if reviewers is not None:
            data['reviewers'] = reviewers
        return self._client.put(self.url(), data=data)

    @response_or_error
    def activities(self, fromId=None, fromType=None):
        """
        Retrieve a page of activity associated with a pull request.

        Activity items include comments, approvals, rescopes (i.e. adding and removing of commits), merges and more.

        Different types of activity items may be introduced in newer versions of Stash or by user installed plugins,
        so clients should be flexible enough to handle unexpected entity shapes in the returned page.

        fromId: (optional) the id of the activity item to use as the first item in the returned page
        fromType: (required if fromId is present) the type of the activity item specified by fromId
        """
        params = dict()
        if fromId is not None:
            if fromType is None:
                raise ValueError("fromType is required when fromId is supplied")
            params['fromId'] = fromId
            params['fromType'] = fromType
        return self._client.get(self.url("/activities"), params=params)

    @ok_or_error
    def decline(self, version=-1):
        """Decline a pull request."""
        return self._client.post(self.url("/decline"), params=dict(version=version))

    @ok_or_error
    def can_merge(self):
        """
        Test whether a pull request can be merged.

        A pull request may not be merged if:

            * there are conflicts that need to be manually resolved before merging; and/or
            * one or more merge checks have vetoed the merge.
        """
        return self._client.get(self.url("/merge"))

    @response_or_error
    def merge(self, version=-1):
        """
        Merge the specified pull request.
        """
        return self._client.post(self.url("/merge"), params=dict(version=version))

    @response_or_error
    def reopen(self, version=-1):
        """
        Re-open a declined pull request.
        """
        return self._client.post(self.url("/reopen"), params=dict(version=version))

    @response_or_error
    def approve(self):
        """
        Approve a pull request as the current user. Implicitly adds the user as a participant if they are not already.
        """
        return self._client.post(self.url("/approve"))

    @response_or_error
    def unapprove(self):
        """
        Remove approval from a pull request as the current user. This does not remove the user as a participant.
        """
        return self._client.delete(self.url("/approve"))

    def changes(self):
        """
        Gets changes for the specified PullRequest.

        Note: This resource is currently not paged. The server will return at most one page.
        The server will truncate the number of changes to an internal maximum.
        """
        return self.paginate("/changes")

    @response_or_error
    def commits(self):
        """
        Retrieve changesets for the specified pull request.
        """
        return self.paginate('/commits')


class PullRequests(ResourceBase, IterableResource):
    def all(self, direction='INCOMING', at=None, state='OPEN', order=None):
        """
        Retrieve pull requests to or from the specified repository.

        direction: (optional, defaults to INCOMING) the direction relative to the specified repository.
            Either INCOMING or OUTGOING.
        at: (optional) a specific branch to find pull requests to or from.
        state: (optional, defaults to OPEN) only pull requests in the specified state will be returned.
            Either OPEN, DECLINED or MERGED.
        order: (optional) the order to return pull requests in, either OLDEST (as in: "oldest first") or NEWEST.
        """

        params = {}

        if direction is not None:
            params['direction'] = direction
        if at is not None:
            params['at'] = at
        if state is not None:
            params['state'] = state
        if order is not None:
            params['order'] = order

        return self.paginate("", params=params)

    def _make_ref(self, ref, refName="the ref"):
        if isinstance(ref, basestring):
            repo = self._parent.get()
            return PullRequestRef(repo['project']['key'], repo['slug'], ref).to_dict()
        elif isinstance(ref, PullRequestRef):
            return ref.to_dict()
        elif isinstance(ref, dict):
            return ref
        else:
            raise ValueError(refName + " should be either a string, a dict, or a PullRequestRef")

    @response_or_error
    def create(self, title, fromRef, toRef, description='', state='OPEN', reviewers=None):
        """
        Create a new pull request between two branches.
        """
        data = dict(title=title,
                    description=description,
                    fromRef=self._make_ref(fromRef, "fromRef"),
                    toRef=self._make_ref(toRef, "toRef"),
                    state=state)

        if reviewers is not None:
            data['reviewers'] = []
            for reviewer in reviewers:
                data['reviewers'].append({"user": dict(name=reviewer)})

        return self._client.post(self.url(""), data=data)

    def __getitem__(self, item):
        """
        Return a specific pull requests
        """
        return PullRequest(item, self.url(item), self._client, self)


