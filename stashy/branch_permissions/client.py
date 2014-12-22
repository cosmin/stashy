from ..client import StashClient

class BranchPermissionsClient(StashClient):
    api_version = '1.0'
    def __init__(self, base_url, session):
        super(BranchPermissionsClient, self).__init__(base_url, session=session)
        self._api_base = self._base_url + "/rest/branch-permissions/" + self.api_version
