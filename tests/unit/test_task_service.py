from unittest.mock import MagicMock, patch

import pytest

from src.api.modules.tasks.schema import (
    TaskFilterRequest,
    TaskRequest,
    TaskResponse,
    TaskUpdateIdUserRequest,
    TaskUpdateRequest,
    TaskUpdateStatusRequest,
)
from src.application.services.task_service import TaskUseCase


class TestTaskUseCase:
    @pytest.fixture
    def task_service(self):
        mock_repo = MagicMock()
        return TaskUseCase(mock_repo)

    @pytest.fixture
    def task_request(self):
        return TaskRequest(
            title="Test Task",
            description="Test Description",
            status="Pending",
            priority="Medium",
            completeness="0%",
            id_list_task=1,
        )

    @pytest.fixture
    def task_response(self):
        return TaskResponse(
            id_task=1,
            title="Test Task",
            description="Test Description",
            status="Pending",
            priority="Medium",
            completeness="0%",
            id_user=1,
            id_list_task=1,
        )

    def test_get_tasks_success(self, task_service, task_response):
        task_service.repo.get_tasks.return_value = [task_response]

        result = task_service.get_tasks()

        assert len(result) == 1
        assert result[0].title == task_response.title

    def test_create_task_success(self, task_service, task_request, task_response):
        task_service.repo.create_task.return_value = task_response

        result = task_service.create_task(task_request)

        assert result == task_response
        task_service.repo.create_task.assert_called_once()

    def test_update_task_success(self, task_service, task_response):
        task_id = 1
        update_request = TaskUpdateRequest(title="Updated Task")
        task_service.repo.update_task.return_value = task_response

        result = task_service.update_task(task_id, update_request)

        assert result == task_response
        task_service.repo.update_task.assert_called_once_with(task_id, update_request)

    def test_delete_task_success(self, task_service):
        task_id = 1
        task_service.repo.delete_task.return_value = None

        task_service.delete_task(task_id)

        task_service.repo.delete_task.assert_called_once_with(task_id)

    def test_get_task_by_id_success(self, task_service, task_response):
        task_id = 1
        task_service.repo.get_task_by_id.return_value = task_response

        result = task_service.get_task_by_id(task_id)

        assert result == task_response
        task_service.repo.get_task_by_id.assert_called_once_with(task_id)

    def test_get_tasks_by_user_id_success(self, task_service, task_response):
        user_id = 1
        task_service.repo.get_tasks_by_user_id.return_value = [task_response]

        result = task_service.get_tasks_by_user_id(user_id)

        assert len(result) == 1
        task_service.repo.get_tasks_by_user_id.assert_called_once_with(user_id)

    def test_get_tasks_by_list_task_id_success(self, task_service, task_response):
        list_task_id = 1
        task_service.repo.get_tasks_by_list_task_id.return_value = [task_response]

        result = task_service.get_tasks_by_list_task_id(list_task_id)

        assert len(result) == 1
        task_service.repo.get_tasks_by_list_task_id.assert_called_once_with(
            list_task_id
        )

    def test_get_filtered_tasks_by_list_task_id_success(
        self, task_service, task_response
    ):
        list_task_id = 1
        filter_request = TaskFilterRequest(status="Pending")
        task_service.repo.get_filtered_tasks_by_list_task_id.return_value = [
            task_response
        ]

        result = task_service.get_filtered_tasks_by_list_task_id(
            list_task_id, filter_request
        )

        assert len(result) == 1
        task_service.repo.get_filtered_tasks_by_list_task_id.assert_called_once_with(
            list_task_id, filter_request
        )

    def test_update_task_status_success(self, task_service, task_response):
        task_id = 1
        status_request = TaskUpdateStatusRequest(status="Completed")
        task_service.repo.update_task_status.return_value = task_response

        result = task_service.update_task_status(task_id, status_request)

        assert result == task_response
        task_service.repo.update_task_status.assert_called_once_with(
            task_id, status_request
        )

    @patch("src.application.services.task_service.send_email")
    def test_update_task_id_user_success(
        self, mock_send_email, task_service, task_response
    ):
        task_id = 1
        email = "user@example.com"
        user_request = TaskUpdateIdUserRequest(id_user=2)
        task_service.repo.update_task_id_user.return_value = task_response
        mock_send_email.return_value = {"id": "email-sent"}

        result = task_service.update_task_id_user(task_id, user_request, email)

        assert result == task_response
        task_service.repo.update_task_id_user.assert_called_once_with(
            task_id, user_request
        )
        mock_send_email.assert_called_once_with(
            email,
            "Task updated",
            f"The task {task_response.title} has been assigned to you, please check it out.",
        )

    @patch("src.application.services.task_service.send_email")
    def test_update_task_id_user_email_error(
        self, mock_send_email, task_service, task_response
    ):
        task_id = 1
        email = "user@example.com"
        user_request = TaskUpdateIdUserRequest(id_user=2)
        task_service.repo.update_task_id_user.return_value = task_response
        mock_send_email.side_effect = Exception("Email service error")

        with pytest.raises(Exception) as exc_info:
            task_service.update_task_id_user(task_id, user_request, email)

        assert "Email service error" in str(exc_info.value)
