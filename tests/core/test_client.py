from unittest import TestCase
from requests import Session
from stashy.core.client import CoreClient


class TestCoreClient(TestCase):
    def test_url_without_slash_prefix(self):
        client = CoreClient("http://example.com/stash", Session())
        self.assertEqual("http://example.com/stash/rest/api/1.0/admin/groups", client.url("admin/groups"))

    def test_url_with_slash_prefix(self):
        client = CoreClient("http://example.com/stash", Session())
        self.assertEqual("http://example.com/stash/rest/api/1.0/admin/groups", client.url("/admin/groups"))
