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
    requests = relationship('TeamRequest', lazy='joined')

    def __repr__(self):
        return '<Team id:{} event_id:{} name:{}>'.format(self.id, self.event_id, self.name)


class TeamMember(DB.Model):
    """TeamMember model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'TeamMembers'

    team_id = DB.Column(DB.Integer, ForeignKey('Teams.id'), nullable=True)
    participant_id = DB.Column(DB.Integer, ForeignKey('Participants.id'), nullable=True)

    # Let a team have many captain, since a captain can accept members
    captain = DB.Column(DB.Boolean, default=False)

    team = relationship("Team", back_populates="members")
    participant = relationship("Participant", backref=backref('teamInfo'))

    def __repr__(self):
        return '<TeamMember id:{} team_id:{} participant_id:{}>'.format(self.id, self.team_id, self.participant_id)


class TeamRequest(DB.Model):
    """TeamRequest model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'TeamRequests'

    team_id = DB.Column(DB.Integer, ForeignKey('Teams.id'), nullable=True)
    participant_id = DB.Column(DB.Integer, ForeignKey('Participants.id'), nullable=True)
    requested_at = DB.Column(DB.DateTime, server_default=DB.func.now())

    team = relationship("Team", back_populates="requests")
    participant = relationship("Participant")

    def __repr__(self):
        return '<TeamRequests id:{} team_id:{} participant_id:{}>'.format(self.id, self.team_id, self.participant_id)
