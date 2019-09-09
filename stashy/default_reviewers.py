from .compat import update_doc
from .errors import response_or_error
from .helpers import ResourceBase, IterableResource, Nested

API_NAME = 'default-reviewers'
API_VERSION = 'latest'
API_OVERRIDE_PATH = '{0}/{1}'.format(API_NAME, API_VERSION)


class Condition(ResourceBase):
    def __init__(self, url, client, parent):
        super(Condition, self).__init__(url, client, parent, API_OVERRIDE_PATH)

    def _url_for(self, cid):
        """
        Alter and expeand a default reviewer url to inlcude a
        reference to a specific condition id (cid).

        Args:
            cid (int): The Pull Request condition id (cid)

        Returns:
            str: A modified Bitbucket default reviewer url
        """
        return self.url(str(cid))

    @response_or_error
    def get(self):
        """
        Retrieve a condition
        """
        return self._client.get(self.url())

    def initialize_def_rev_condition(self, data, headers):
        """
        Initialize a new default reviewer condition with desired default
        reviewer(s).

        Args:
            data (dict): The configuration of Bitbucket settings
            specifying the Pull Request source branch, target branch,
            default reviewers and required approval conditons.

            headers (dict): The HTTP headers which indicate the media
            type of the resource when requesting to change data on
            Bitbucket.

        Returns:
            request.Response: A response instance directly derived
            from the HTTP request to Bitbucket.

        """
        return self._client.post(self.url(), json=data, headers=headers)

    def update_def_rev_condition(self, data, headers, cid):
        """
        Update a preexisting default reviewer condition with desired
        default reviewer(s).

        Args:
            data (dict): The configuration of Bitbucket settings
            specifying the Pull Request source branch, target branch,
            default reviewers and required approval conditons.

            headers (dict): The HTTP headers which indicate the media
            type of the resource when requesting to change data on
            Bitbucket.

            cid (int): The condition id that directs the HTTP request to
            update the preexisting Bitbucket Pull Request condition.

        Returns:
            request.Response: A response instance directly derived
            from the HTTP request to Bitbucket.

        """
        return self._client.put(self._url_for(cid), json=data,
                                headers=headers)

    def delete_def_rev_condition(self, cid):
        """
        Delete a preexisting default reviewer condition.

        Returns:
            request.Response: A response instance directly derived
            from the HTTP request to Bitbucket.

        """
        return self._client.delete(self._url_for(cid))


class Conditions(ResourceBase, IterableResource):

    def __init__(self, url, client, parent):
        ResourceBase.__init__(self, url, client, parent, API_OVERRIDE_PATH)

    def __getitem__(self, item):
        return Condition(item, self.url(item), self._client, self)

    @response_or_error
    def get(self):
        """
        Retrieve a condition
        """
        return self._client.get(self.url())


update_doc(Conditions.all,
           """Retrieve list of default reviewer conditions for a repo""")


class DefaultReviewers(ResourceBase):
    conditions = Nested(Conditions)
    condition = Nested(Condition)
