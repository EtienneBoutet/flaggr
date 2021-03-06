"""Team marshmallow schemas"""

from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.participant import ParticipantSchema


class TeamMemberSchema(Schema):
    """Schema for getting a team member's information"""
    participant = fields.Nested(ParticipantSchema)
    captain = fields.Bool()


class TeamWithoutRequestsSchema(Schema):
    """Schema for a team without the join requests"""
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    name = fields.String(required=True)

    members = fields.Nested(TeamMemberSchema, many=True)


class TeamRequestSchema(Schema):
    """Schema that represents a team request"""
    participant = fields.Nested(ParticipantSchema)
    team = fields.Nested(TeamWithoutRequestsSchema, required=True)
    requested_at = fields.DateTime()


class TeamSchema(Schema):
    """Schema for getting a team's information"""
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    name = fields.String(required=True)

    members = fields.Nested(TeamMemberSchema, many=True)
    requests = fields.Nested(TeamRequestSchema, many=True)


class TeamBasicInfoSchema(Schema):
    """Schema for getting a team's basic information"""
    name = fields.String(required=True)


class CreateTeamRequestSchema(RequestSchema):
    """Request schema to create a team request"""
    team_name = fields.String(required=True)


class SendTeamRequestRequestSchema(RequestSchema):
    """Request schema to request to join a team"""
    team_id = fields.Integer(required=True)


class AcceptTeamRequestRequestSchema(RequestSchema):
    """Request schema when accepting a team request"""
    participant_id = fields.Integer(required=True)


class DeclineTeamRequestRequestSchema(RequestSchema):
    """Request schema when declining a team request"""
    participant_id = fields.Integer(required=True)


class KickTeamMemberRequestSchema(RequestSchema):
    """Request schema when kicking a team member"""
    participant_id = fields.Integer(required=True)


class ChangeRoleRequestSchema(RequestSchema):
    """Request schema when changing a team member's role"""
    participant_id = fields.Integer(required=True)
    captain = fields.Bool(required=True)
