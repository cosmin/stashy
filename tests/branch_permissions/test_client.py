from unittest import TestCase
from requests import Session
from stashy.branch_permissions.client import BranchPermissionsClient


class TestBranchPermissionsClient(TestCase):
    def test_url(self):
        client = BranchPermissionsClient("http://example.com/stash", Session())
        self.assertEqual("http://example.com/stash/rest/branch-permissions/1.0/", client.url("/"))
