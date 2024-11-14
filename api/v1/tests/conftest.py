#!/usr/bin/python3

"""
Test configuration file for pytest
"""

from api.db.database import get_session
from api.v1.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, RoleChecker
from unittest.mock import Mock
from api import app
import pytest
from fastapi.testclient import TestClient


mock_session = Mock()
mock_user_service = Mock()
mock_task_service = Mock()


def get_mock_session():
    """Get mock session"""
    yield mock_session


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(["admin", "user"])

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[refresh_token_bearer] = Mock()
app.dependency_overrides[access_token_bearer] = Mock()
app.dependency_overrides[role_checker] = Mock()


@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_user_service():
    return mock_user_service


@pytest.fixture
def fake_task_service():
    return mock_task_service


@pytest.fixture
def test_client():
    return TestClient(app)
