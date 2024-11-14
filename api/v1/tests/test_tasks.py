#!/usr/bin/python3
"""test Task Module"""

tasks_prefix = f"/api/v1/tasks"


def test_get_tasks(test_client, fake_task_service, fake_session):
    """Test get tasks"""

    response = test_client.get(url=f"{tasks_prefix}")

    assert fake_task_service.get_tasks_called_once()
    assert fake_task_service.get_tasks_called_once_with(fake_session)

def test_create_task(test_client, fake_task_service, fake_session):
    """Test create tasks"""

    task_data = {
        "title": "test title",
        "description": "test description",
        "due_date": "2023-01-01",
        "status": "todo",
        "priority": "high",
        "assigned_to": "naddulidaniel@gmail.com ",
        "tags": ["test", "tag"],
    }

    response = test_client.post(url=f"{tasks_prefix}", json=task_data)

    assert fake_task_service.create_task_called_once()
    assert fake_task_service.create_task_called_once_with(task_data, fake_session)
