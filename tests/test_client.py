from unittest import TestCase
from stashy.client import StashClient


class TestStashClient(TestCase):
    def test_url_without_slash_prefix(self):
        client = StashClient("http://example.com/stash")
        self.assertEqual("http://example.com/stash/rest/api/1.0/admin/groups", client.url("api/1.0/admin/groups"))

    def test_url_with_slash_prefix(self):
        client = StashClient("http://example.com/stash")
        self.assertEqual("http://example.com/stash/rest/api/1.0/admin/groups", client.url("/api/1.0/admin/groups"))
