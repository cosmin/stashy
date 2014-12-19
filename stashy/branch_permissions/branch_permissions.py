from ..helpers import ResourceBase, IterableResource
from ..errors import ok_or_error, response_or_error
from ..compat import update_doc


class Permitted(ResourceBase, IterableResource):
    pass

update_doc(Permitted.all, """Retrieve projects.""")
