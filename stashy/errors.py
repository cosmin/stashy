from functools import wraps
from decorator import decorator

class NotFoundException(Exception):
    def __init__(self, response):
        try:
            self.data = response.json()
            if 'errors' in self.data:
                msg = self.data['errors'][0]['message']
            else:
                msg = str(self.data)
        except ValueError:
            msg = "Not found: " + response.url

        super(NotFoundException, self).__init__(msg)


class GenericException(Exception):
    def __init__(self, response):
        try:
            self.data = response.json()
            msg = "%d: %s" % (response.status_code, self.data)
        except ValueError:
            msg = "Unknown error: %d(%s)" % (response.status_code, response.reason)

        super(GenericException, self).__init__(msg)


class AuthenticationException(Exception):
    def __init__(self, response):
        try:
            msg = "%d: Invalid User / Password" % response.status_code
        except ValueError:
            msg = "Invalid Authentication" 

        super(AuthenticationException,self).__init__(msg)

def maybe_throw(response):
    if not response.ok:
        if response.status_code == 404:
            raise NotFoundException(response)
        elif response.status_code == 401:
            raise AuthenticationException(response)
        else:
            e = GenericException(response)
            try:
                e.data = response.json()
            except ValueError:
                e.content = response.content
            raise e


@decorator
def ok_or_error(fn, *args, **kw):
    response = fn(*args, **kw)
    maybe_throw(response)
    return response.ok


@decorator
def response_or_error(fn, *args, **kw):
    response = fn(*args, **kw)
    maybe_throw(response)
    try:
        return response.json()
    except ValueError:
        return response.text
