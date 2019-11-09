"""'Flags' SQLAlchemy model"""

from sqlalchemy import ForeignKey

from JDISCTF.app import DB


class Flag(DB.Model):
    """
    Flag model

    A flag is the answer to an event's challenge. Participants must input it into the platform in
    order to be awarded points.
    """

    __tablename__ = 'Flags'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the flag. Should be generated by the database. Used as primary key."""
    challenge_id = DB.Column(DB.Integer, ForeignKey('Challenges.id'), nullable=True)
    """The ID of the challenge the flag belongs to. Used as foreign key."""
    is_regex = DB.Column(DB.Boolean)
    """Whether or not the flag should be evaluated as a regex or as a plain string."""
    value = DB.Column(DB.String)
    """The actual value of the flag"""

    def __repr__(self):
        return '<Flag id:{} challenge_id:{} is_regex:{} value:{}>' \
            .format(self.id, self.challenge_id, self.is_regex, self.value)
