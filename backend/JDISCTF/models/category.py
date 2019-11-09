"""'Categories' SQLAlchemy model"""

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from JDISCTF.app import DB


class Category(DB.Model):
    """
    Category model

    A category groups challenges together under a common theme (programming, web, etc).
    A category is associated to a single event and should have a unique name within that event
    (events A and B can both have a category C, but event A cannot have two categories C).
    """

    __tablename__ = 'Categories'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the category. Should be generated by the database. Used as primary key."""
    event_id = DB.Column(DB.Integer, ForeignKey('Events.id'), nullable=True)
    """The ID of the event the category belongs to. Used as foreign key."""
    name = DB.Column(DB.String(64), index=True)
    """The name of the category. Max 64 characters."""

    __table_args__ = (
        UniqueConstraint('event_id', 'name', name='categories_event_name_uc'),
    )

    challenges = relationship('Challenge', lazy='noload')

    def __repr__(self):
        return '<Category id:{} event_id:{} name:{}'.format(self.id, self.event_id, self.name)
