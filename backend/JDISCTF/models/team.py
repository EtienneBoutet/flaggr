"""Teams' SQLAlchemy model"""

from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import backref, relationship

from JDISCTF.app import DB


class Team(DB.Model):
    """
    Team model

    A team is a grouping of participants who compete together. A team must always have at least one
    member.
    """
    __tablename__ = 'Teams'
    __table_args__ = (
        UniqueConstraint('event_id', 'name', name='team_event_name_uc'),
    )

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the team. Should be generated by the database. Used as primary key."""
    event_id = DB.Column(DB.Integer, ForeignKey('Events.id'), nullable=True)
    """The ID of the event the team is registered to. Used as foreign key."""
    name = DB.Column(DB.String(64), index=True)
    """The name of the team. Two teams competing in the same event cannot have the same name."""

    members = relationship('TeamMember', lazy="joined", back_populates="team")
    submissions = relationship('Submission', lazy="joined", back_populates="team")
    requests = relationship('TeamRequest', lazy='joined')

    def __repr__(self):
        return '<Team id:{} event_id:{} name:{}>'.format(self.id, self.event_id, self.name)

    def __eq__(self, other):
        return self.id == other.id and \
            self.event_id == other.event_id and \
            self.name == other.name

    def __hash__(self):
        return hash(self.__dict__.values())


class TeamMember(DB.Model):
    """TeamMember model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'TeamMembers'

    team_id = DB.Column(DB.Integer, ForeignKey('Teams.id'), nullable=True)
    user_id = DB.Column(DB.Integer, ForeignKey('Users.id'), nullable=True)

    # Let a team have many captains
    captain = DB.Column(DB.Boolean, default=False)

    team = relationship("Team", back_populates="members")
    user = relationship("User", backref=backref("teamInfo"))

    def __repr__(self):
        return '<TeamMember id:{} team_id:{} user_id:{}>'.format(self.id, self.team_id, self.user_id)

    def __eq__(self, other):
        return self.team_id == other.team_id and \
            self.user_id == other.user_id and \
            self.captain == other.captain

    def __hash__(self):
        return hash(self.__dict__.values())


class TeamRequest(DB.Model):
    """TeamRequest model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'TeamRequests'

    team_id = DB.Column(DB.Integer, ForeignKey('Teams.id'), nullable=True)
    user_id = DB.Column(DB.Integer, ForeignKey('Users.id'), nullable=True)
    requested_at = DB.Column(DB.DateTime, server_default=DB.func.now())

    team = relationship("Team", back_populates="requests")
    user = relationship("User")

    def __repr__(self):
        return '<TeamRequests id:{} team_id:{} user_id:{}>'.format(self.id, self.team_id, self.user_id)

    def __eq__(self, other):
        return self.id == other.id and \
            self.team_id == other.team_id and \
            self.user_id == other.user_id and \
            self.requested_at == other.requested_at

    def __hash__(self):
        return hash(self.__dict__.values())
