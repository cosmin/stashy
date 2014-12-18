from ..helpers import Nested, ResourceBase

from .groups import Groups
from .users import Users
from ..permissions import Permissions


class Admin(ResourceBase):
    groups = Nested(Groups)
    users = Nested(Users)
    permissions = Nested(Permissions)
