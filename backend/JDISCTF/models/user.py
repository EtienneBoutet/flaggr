"""'User' SQLAlchemy model"""

from __future__ import annotations

from base64 import b64decode
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from JDISCTF.app import Config, DB, LOGIN_MANAGER
from JDISCTF.models.team import Team
from JDISCTF.models.participant import Participant


class User(UserMixin, DB.Model):
    """
    User model

    A user of the application (event participant or admin). A user is only represented by its username and
    authenticates on the platform with its email and password.
    """

    __tablename__ = 'Users'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the user. Should be generated by the database. Used as primary key."""
    email = DB.Column(DB.String(255), index=True, unique=True)
    """The user's email. Unique. Max 255 characters."""
    username = DB.Column(DB.String(64), index=True, unique=True)
    """The user's display name. Unique. Max 64 characters."""
    password_hash = DB.Column(DB.String(128))
    """
    The hash of the user's password. Should always be set with the 'set_password' method. Max
    128 characters.
    """

    def __repr__(self):
        return '<User id:{} email:{} username:{}>'.format(self.id, self.email, self.username)

    def set_password(self, password: str):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check whether or not this is the user's password"""
        return check_password_hash(self.password_hash, password)

    def get_team(self) -> Optional[Team]:
        participant = self.get_participant()
        return None if not participant else participant.get_team()

    def get_participant(self) -> Optional[Participant]:
        return Participant.query.filter_by(user_id=self.id).first()


if Config.DEBUG:
    @LOGIN_MANAGER.request_loader
    def load_user_from_request(request):
        # pylint: disable=bare-except
        """
        DEVELOPMENT ONLY. Returns a User class from an authorization header.
        Required by flask-login
        """

        try:
            auth_header = request.headers.get("Authorization")
            auth_header = auth_header.replace('Basic ', '', 1)

            auth_header = b64decode(auth_header)
            email, password = auth_header.split(b":", 1)
            email = email.decode()
            password = password.decode()
        except:
            return None

        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password_hash, password):
            return None

        return user


@LOGIN_MANAGER.user_loader
def load_user(user_id: str) -> User:
    """Returns a User class from a user id. Required by flask-login"""
    return User.query.get(int(user_id))
