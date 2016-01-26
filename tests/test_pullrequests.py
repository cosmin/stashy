import json
import os
from unittest import TestCase
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from requests.models import Response
from mock import patch

from stashy.client import StashClient
from stashy.pullrequests import PullRequest


def fake_urlopen(stash_client, url):
    """
    A stub urlopen() implementation that load json responses from
    the filesystem.
    """
    # Map path from url to a file
    parsed_url = urlparse(url)
    resource_file = os.path.normpath(
        '%s/resources/%s.json' % (os.path.dirname(os.path.abspath(__file__)), parsed_url.path))
    # Must return Response
    resp = Response()
    resp.status_code = 200
    resp.json = lambda: json.loads(open(resource_file, mode='rb').read().decode('utf-8'))
    return resp


class TestPullRequest(TestCase):
    def setUp(self):
        self.client = StashClient("http://example.com/stash")

    @patch('stashy.client.StashClient.get', fake_urlopen)
    def test_can_merge(self):
        pr = PullRequest(1, '', self.client, None)
        assert pr.can_merge() is False

    @patch('stashy.client.StashClient.get', fake_urlopen)
    def test_merge_vetoes(self):
        pr = PullRequest(1, '', self.client, None)
        vetoes = pr.merge_info()

        assert len(vetoes['vetoes']) == 1
