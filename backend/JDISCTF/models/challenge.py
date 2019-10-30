"""'Challenges' SQLAlchemy model"""

from JDISCTF.app import DB
from sqlalchemy import ForeignKey


class Challenge(DB.Model):
    """
    Challenge model

    A challenge an event participant has to solve. A challenge is always associated with a
    category and is composed of a (relatively) short name, an arbitrarily long description (which
    might include nothing at all, or a very complex, multi-chapter backstory, and a number of points
    to be awarded upon challenge completion.

    A challenge may also be hidden from event participants if it is for example in a draft stage or
    simply not yet released.
    """

    __tablename__ = 'Challenges'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the challenge. Should be generated by the database. Used as primary key."""
    category_id = DB.Column(DB.Integer, ForeignKey('Categories.id'), nullable=True)
    """The ID of the category the challenge belongs to. Used as foreign key."""
    name = DB.Column(DB.String(255), index=True)
    """The name of the challenge. Max 255 characters."""
    description = DB.Column(DB.Text())
    """The description of the event. Can be arbitrarily long."""
    points = DB.Column(DB.Integer)
    """The number of points the challenge is worth."""
    hidden = DB.Column(DB.Boolean)
    """Whether or not the challenge should be visible by the event participants."""

    def __repr__(self):
        return '<Challenge id:{} category_id:{} name:{} description:{} points:{}>'\
            .format(self.id, self.category_id, self.name, self.description, self.points)