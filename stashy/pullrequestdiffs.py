from .diffs import Diff
from .helpers import ResourceBase
from .errors import response_or_error


class PullRequestDiffRef(object):
    def __init__(self, project_key, repo_slug, id):
        self.project_key = project_key
        self.repo_slug = repo_slug
        self.id = id

    def to_dict(self):
        return dict(id=self.id,
                    repository=dict(slug=self.repo_slug,
                                    project=dict(key=self.project_key),
                                    name=self.repo_slug))


class PullRequestDiff(ResourceBase):
    def __init__(self, url, client, parent):
        super(PullRequestDiff, self).__init__(url, client, parent)
        response = self.get()
        self.from_hash = response["fromHash"]
        self.to_hash = response["toHash"]
        self.context_lines = response["contextLines"]
        self.whitespace = response["whitespace"]
        self.diffs = []
        for value in list(response["diffs"]):
            self.diffs.append(Diff(value))

    @response_or_error
    def get(self):
        return self._client.get(self.url())

    def _get_from_hash(self):
        return self._from_hash

    def _set_from_hash(self, value):
        self._from_hash = value

    def _get_to_hash(self):
        return self._to_hash

    def _set_to_hash(self, value):
        self._to_hash = value

    def _get_diffs(self):
        return self._diffs

    def _set_diffs(self, value):
        self._diffs = value

    def _get_context_lines(self):
        return self._context_lines

    def _set_context_lines(self, value):
        self._context_lines = value

    def _get_whitespace(self):
        return self._whitespace

    def _set_whitespace(self, value):
        self._whitespace = value

    from_hash = property(_get_from_hash, _set_from_hash)

    to_hash = property(_get_to_hash, _set_to_hash)

    diffs = property(_get_diffs, _set_diffs)

    context_lines = property(_get_context_lines, _set_context_lines)

    whitespace = property(_get_whitespace, _set_whitespace)
