#!/usr/bin/python3
"""Test authentication module"""

from api.v1.auth.schema import UserCreate


auth_prefix = f"/api/v1/auth"


def test_user_creation(fake_session, fake_user_service, test_client):
    """Test user creation"""
    signup_data = {
        "username": "nadduli",
        "email": "naddulidaniel1994@gmail.com",
        "password": "innocent",
    }

    response = test_client.post(url=f"{auth_prefix}/register", json=signup_data)

    user_data = UserCreate(**signup_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(
        signup_data["email"], fake_session
    )
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(user_data, fake_session)
