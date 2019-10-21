"""Users routes"""

from flask_rebar import errors
from JDISCTF.app import REGISTRY
from JDISCTF.models import User
from JDISCTF.schemas import USERS_SCHEMA, USER_SCHEMA


@REGISTRY.handles(
    rule="/users",
    method="GET",
    response_body_schema=USERS_SCHEMA
)
def get_all_users():
    """DEVELOPMENT ROUTE. Gets all the users, non-paginated"""
    user = User.query.all()

    return user

@REGISTRY.handles(
    rule="/users/<int:user_id>",
    method="GET",
    response_body_schema=USER_SCHEMA
)
def get_user(user_id: int):
    """Get a user's info by its id"""
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise errors.NotFound()

    return user