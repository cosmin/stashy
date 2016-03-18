from .errors import maybe_throw


def add_json_headers(kw):
    if 'headers' not in kw:
        kw['headers'] = {}

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    for header, value in headers.items():
        kw['headers'][header] = value

    return kw


class ResourceBase(object):
    def __init__(self, url, client, parent, api_path=None,
                 branches_api_path=None):
        self._client = client
        self._parent = parent
        if api_path is None:
            api_path = self._client.core_api_path
            branches_api_path = self._client.branches_api_path
        if branches_api_path is None:
            branches_api_path = self._client.branches_api_path

        # make sure we're only prefixing with one api path
        if url.startswith(api_path):
            self._url = url
            self._branchesurl = url.replace(api_path, branches_api_path)
        elif url.startswith(self._client.core_api_path):
            self._url = url.replace(self._client.core_api_path, api_path)
            self._branchesurl = url.replace(self._client.core_api_path,
                                            branches_api_path)
        else:
            if url.startswith('/'):
                url = url[1:]
            self._url = '{0}/{1}'.format(api_path, url)
            self._branchesurl = '{0}/{1}'.format(branches_api_path, url)




    def url(self, resource_url="", is_branches=False):
        if resource_url and not resource_url.startswith("/"):
            resource_url = "/" + resource_url
        if is_branches:
            if self._url.endswith("/"):
                url = self._branchesurl[:-1]
            else :
                url = self._branchesurl
        else:
            if self._url.endswith("/"):
                url = self._url[:-1]
            else :
                url = self._url
        return url + resource_url

    def paginate(self, resource_url, params=None, values_key='values',
                 is_branches=False):
        url = self.url(resource_url, is_branches)

        more = True
        start = None
        while more:
            kw = {}
            if params:
                kw['params'] = params
            if start is not None:
                kw.setdefault('params', {})
                kw['params']['start'] = start

            response = self._client.get(url, **kw)
            maybe_throw(response)

            data = response.json()

            if not values_key in data:
                return
            for item in data[values_key]:
                yield item

            if data['isLastPage']:
                more = False
            else:
                more = True
                start = data['nextPageStart']


class IterableResource(object):
    def __iter__(self):
        """
        Convenience method around self.all()
        """
        return self.all()

    def all(self):
        """
        Retrieve all the resources.
        """
        return self.paginate("")

    def list(self):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        return list(self.all())


class FilteredIterableResource(IterableResource):
    def all(self, filter=None):
        """
        Retrieve all the resources, optionally modified by filter.
        """
        params = {}
        if filter:
            params['filter'] = filter
        return self.paginate("", params)

    def list(self, filter=None):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        return list(self.all(filter))


class Nested(object):
    def __init__(self, cls, relative_path=''):

        # nested object for clarity of usage, no effect on resource url
        if relative_path is None:
            self.relative_path = ''

        # default case, use lowercase class name
        elif not relative_path:
            self.relative_path = "/%s" % cls.__name__.lower()

        # explicit override of relative path
        else:
            if not relative_path.startswith("/"):
                relative_path = "/" + relative_path
            self.relative_path = relative_path
        self.cls = cls

    def __get__(self, instance, kind):
        parent_url = instance._url
        if parent_url.endswith("/"):
            parent_url = parent_url[:-1]

        url = parent_url + self.relative_path
        return self.cls(url=url, client=instance._client, parent=instance)

