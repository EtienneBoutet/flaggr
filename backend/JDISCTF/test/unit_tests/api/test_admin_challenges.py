from unittest.mock import MagicMock, patch

from flask_rebar import errors
from pytest import fixture, raises

from JDISCTF.api.admin import challenges
from JDISCTF.models import Category, Challenge, Event, Flag, Submission, Team, User


def local_patch(module: str):
    return patch("JDISCTF.api.admin.challenges." + module)


@fixture
def event_mock():
    with local_patch("Event") as mock:
        yield mock


@fixture
def category_mock():
    with local_patch("Category") as mock:
        yield mock


@fixture
def challenge_mock():
    with local_patch("Challenge") as mock:
        yield mock


@fixture
def flag_mock():
    with local_patch("Flag") as mock:
        yield mock


@fixture
def rebar_mock():
    with local_patch("flask_rebar") as mock:
        yield mock


@fixture
def db_mock():
    with local_patch("DB") as mock:
        yield mock


@fixture
def current_user_mock():
    with local_patch("current_user") as mock:
        yield mock

A_CATEGORY = Category(id=0, event_id=0, name="Category")
A_EVENT = Event(id=0, name="Test Event", teams=True)
A_CHALLENGE = Challenge(id=0,name="Challenge name", points=100, hidden=False, description="My description", category_id=A_CATEGORY.id)
A_FLAG = Flag(id=None, challenge_id=A_CHALLENGE.id, is_regex=False, value="JDIS-FLAG")

class TestGetChallenge:
    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        yield db_mock

    @fixture(autouse=True)
    def _challenge_mock(self, challenge_mock: MagicMock):
        challenge_mock.side_effect = lambda *args, **kwargs: Challenge(*args, **kwargs)

    def test_given_non_existent_challenge_id_should_raise_not_found_error(self, challenge_mock: MagicMock, flag_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        flag_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.NotFound):
            challenges.get_admin_challenge(-1)

    def test_should_return_challenge(self, challenge_mock: MagicMock, flag_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = A_CHALLENGE
        flag_mock.query.filter_by.return_value.all.return_value = A_FLAG

        result = challenges.get_admin_challenge(1)
        assert result == {"challenge": A_CHALLENGE, "flags": A_FLAG}


class TestCreateChallenge:
    REQUEST_BODY = {"name": "New challenge", "points": 100, "hidden": False, "description": "New Description", "category_id": 0}
    A_NEW_CHALLENGE = Challenge(id=None, name=REQUEST_BODY["name"], points=REQUEST_BODY["points"],hidden=REQUEST_BODY["hidden"],
                                description=REQUEST_BODY["description"], category_id=REQUEST_BODY["category_id"])

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        yield db_mock

    @fixture(autouse=True)
    def _challenge_mock(self, challenge_mock: MagicMock):
        challenge_mock.side_effect = lambda *args, **kwargs: Challenge(*args, **kwargs)

    def test_given_already_used_name_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = A_CHALLENGE

        with raises(errors.UnprocessableEntity):
            challenges.create_challenge()

    def test_given_blank_name_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock, rebar_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        rebar_mock.get_validated_body.return_value = \
            {"name": "", "points": 100, "hidden": False, "description": "New Description", "category_id": 0}

        with raises(errors.UnprocessableEntity):
            challenges.create_challenge()

    def test_given_negative_points_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock, rebar_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        rebar_mock.get_validated_body.return_value = \
            {"name": "A Name", "points": -1, "hidden": False, "description": "New Description", "category_id": 0}

        with raises(errors.UnprocessableEntity):
            challenges.create_challenge()

    def test_given_invalid_category_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock, category_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        category_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            challenges.create_challenge()

    def test_should_create_challenge(self, db_mock: MagicMock, challenge_mock: MagicMock, category_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        category_mock.query.filter_by.return_value.first.return_value = A_CATEGORY

        challenges.create_challenge()

        db_mock.session.add.assert_called_with(self.A_NEW_CHALLENGE)
        db_mock.session.commit.assert_called_once()

    def test_should_return_challenge(self, challenge_mock: MagicMock, category_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None
        category_mock.query.filter_by.return_value.first.return_value = A_CATEGORY

        result = challenges.create_challenge()
        assert result == {"challenge": self.A_NEW_CHALLENGE}

class TestEditChallenge:
    REQUEST_BODY = {"name": "Edited challenge", "points": 999, "hidden": True, "description": "Edited Description", "category_id": 1}
    AN_EDITED_CHALLENGE = Challenge(id=0, name=REQUEST_BODY["name"], points=REQUEST_BODY["points"],hidden=REQUEST_BODY["hidden"],
                                    description=REQUEST_BODY["description"], category_id=REQUEST_BODY["category_id"])

    @fixture(autouse=True)
    def _rebar_mock(self, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = self.REQUEST_BODY
        yield rebar_mock

    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        yield db_mock

    @fixture(autouse=True)
    def _challenge_mock(self, challenge_mock: MagicMock):
        challenge_mock.side_effect = lambda A_CHALLENGE, **kwargs: Challenge(*args, **kwargs)

    def test_given_invalid_challenge_id_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            challenges.edit_challenge(-1)

    def test_given_blank_name_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock, rebar_mock: MagicMock):
        rebar_mock.get_validated_body.return_value = \
            {"name": "", "points": 999, "hidden": True, "description": "Edited Description", "category_id": 1}

        with raises(errors.UnprocessableEntity):
            challenges.edit_challenge(1)

    def test_given_already_used_name_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.side_effect = [A_CHALLENGE, A_CHALLENGE]

        with raises(errors.UnprocessableEntity):
            challenges.edit_challenge(1)

    def test_given_negative_points_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock, rebar_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.side_effect = [A_CHALLENGE, None]

        rebar_mock.get_validated_body.return_value = \
            {"name": "Edited challenge", "points": -1, "hidden": True, "description": "Edited Description", "category_id": 1}

        with raises(errors.UnprocessableEntity):
            challenges.edit_challenge(1)

    def test_given_invalid_category_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock, category_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.side_effect = [A_CHALLENGE, None]
        category_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            challenges.edit_challenge(1)

    def test_should_edit_challenge(self, db_mock: MagicMock, challenge_mock: MagicMock, category_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.side_effect = [A_CHALLENGE, None]
        category_mock.query.filter_by.return_value.first.return_value = A_CATEGORY

        challenges.edit_challenge(1)

        db_mock.session.commit.assert_called_once()

    def test_should_return_challenge(self, challenge_mock: MagicMock, category_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.side_effect = [A_CHALLENGE, None]
        category_mock.query.filter_by.return_value.first.return_value = A_CATEGORY

        result = challenges.edit_challenge(1)
        assert result == {"challenge": self.AN_EDITED_CHALLENGE}

class TestDeleteChallenge:
    @fixture(autouse=True)
    def _db_mock(self, db_mock: MagicMock):
        yield db_mock

    @fixture(autouse=True)
    def _challenge_mock(self, challenge_mock: MagicMock):
        challenge_mock.side_effect = lambda A_CHALLENGE, **kwargs: Challenge(*args, **kwargs)

    def test_given_invalid_challenge_id_should_raise_unprocessable_entity_error(self, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = None

        with raises(errors.UnprocessableEntity):
            challenges.delete_challenge(-1)

    def test_should_delete_challenge(self, db_mock: MagicMock, challenge_mock: MagicMock):
        challenge_mock.query.filter_by.return_value.first.return_value = A_CHALLENGE
        challenges.delete_challenge(1)

        db_mock.session.delete.assert_called_with(A_CHALLENGE)
        db_mock.session.commit.assert_called_once()