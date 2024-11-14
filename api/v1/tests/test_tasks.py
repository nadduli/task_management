#!/usr/bin/python3
"""test Task Module"""

tasks_prefix = f"/api/v1/tasks"


def test_get_tasks(test_client, fake_task_service, fake_session):
    """Test get tasks"""

    response = test_client.get(url=f"{tasks_prefix}")

    assert fake_task_service.get_tasks_called_once()
    assert fake_task_service.get_tasks_called_once_with(fake_session)
