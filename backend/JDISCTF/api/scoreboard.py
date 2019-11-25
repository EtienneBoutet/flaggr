"""Scoreboard routes"""

from flask_rebar import errors
from sqlalchemy import text

from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Event
from JDISCTF.schemas.scoreboard import ScoreboardSchema


@REGISTRY.handles(
    rule="/event/<int:event_id>/scoreboard",
    method="GET",
    response_body_schema=ScoreboardSchema(many=True)
)
def get_scoreboard(event_id: int):
    """Get the scoreboard data"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    query = """
    SELECT ROW_NUMBER() OVER (ORDER BY qq.pointss DESC) AS "position",
       qq.team_id, qq.pointss AS points, qq.team_name, qq.last_submission, qq.solved_challenges
    FROM (
    SELECT team_id, SUM(points) AS "pointss", team_name, MAX(submission_time) AS "last_submission", COUNT(challenge_id) as "solved_challenges"
    FROM (
        SELECT DISTINCT ON (s.challenge_id)
             s.team_id AS "team_id", t.name AS "team_name",
           s.challenge_id AS "challenge_id", c.points as "points", s.time AS "submission_time"
        FROM "Submissions" s
        JOIN "Teams" t ON t.id = s.team_id
        JOIN "Challenges" c on c.id = s.challenge_id
        WHERE s.is_correct = true
            AND t.event_id = :e
    ) AS q
    GROUP BY q.team_id, q.team_name
    ) as qq
    ORDER BY pointss DESC
    """

    result = list(DB.engine.execute(text(query), e=event_id))
    return list(map(dict, result))
