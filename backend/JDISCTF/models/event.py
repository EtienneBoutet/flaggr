"""Events' SQLAlchemy model"""
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from JDISCTF.app import DB


class Event(DB.Model):
    """
    Event model

    The core of the application. An event's only defining characteristic is its name, which must be
    unique (i.e. 'CS Games 2019', 'United CTF 2019', etc). The rest is all handled by relations with
    the application's other models.
    """

    __tablename__ = 'Events'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the event. Should be generated by the database. Used as primary key."""
    name = DB.Column(DB.String(64), index=True, unique=True)
    """The name of the event. Max 64 characters."""
    front_page = DB.Column(DB.Text())
    """The front page content of the event. Markdown text that will be parsed by frontend."""
    teams = DB.Column(DB.Boolean)
    """Whether participants have to register as teams or individually."""
    url = DB.Column(DB.String(255), default="")
    """The URL of the event."""
    flag_format = DB.Column(DB.String(64), default="")
    """The flag format used by most challenges."""
    is_open = DB.Column(DB.Boolean, default=False)
    """Whether flag submission is open or not."""
    is_visible = DB.Column(DB.Boolean, default=False)
    """Whether the event is currently visible or not."""


    event_administrators = relationship('EventAdministrator', back_populates='event')
    administrators = association_proxy('event_administrators', 'administrator')

    def __repr__(self):
        return '<Event id:{} name:{} teams: {}>'.format(self.id, self.name, self.teams)

    def __eq__(self, other):
        return self.id == other.id and \
               self.name == other.name and \
               self.front_page == other.front_page and \
               self.teams == other.teams and \
               self.url == other.url and \
               self.flag_format == other.flag_format and \
               self.is_open == other.is_open and \
               self.is_visible == other.is_visible
