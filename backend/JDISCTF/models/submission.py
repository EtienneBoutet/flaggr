"""'Submissions' SQLAlchemy model"""

from sqlalchemy import ForeignKey, func

from JDISCTF.app import DB


class Submission(DB.Model):
    """
    Submission model

    A submission is an attempt from an event participant to solve a challenge.
    """

    __tablename__ = 'Submissions'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the submission. Should be generated by the database. Used as primary key."""
    team_id = DB.Column(DB.Integer, ForeignKey('Teams.id'), nullable=True)
    """The ID of the team who made the submission. Used as foreign key."""
    challenge_id = DB.Column(DB.Integer, ForeignKey('Challenges.id'), nullable=True)
    """The ID of the challenge that this submission attempted to solve. Used as foreign key."""
    input = DB.Column(DB.String(64))
    """The solution that was submitted."""
    is_correct = DB.Column(DB.Boolean)
    """Whether or not the submission is correct."""
    time = DB.Column(DB.DateTime, server_default=func.now())
    """The date and time of the submission."""

    def __repr__(self):
        return '<Submission id:{} team_id:{} challenge_id:{} input:{} is_correct:{}>'\
            .format(self.id, self.team_id, self.challenge_id, self.input, self.is_correct)

    def __eq__(self, other):
        return self.id == other.id and \
            self.team_id == other.team_id and \
            self.challenge_id == other.challenge_id and \
            self.input == other.input and \
            self.is_correct == other.is_correct and \
            self.time == other.time
