from ..client import StashClient

class CoreClient(StashClient):
    api_version = '1.0'
    def __init__(self, base_url, session):
        super(CoreClient, self).__init__(base_url, session=session)
        self._api_base = self._base_url + "/rest/api/" + self.api_version
