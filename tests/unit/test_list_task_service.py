from unittest.mock import MagicMock

import pytest

from src.api.modules.list_tasks.schema import (
    ListTaskRequest,
    ListTaskResponse,
    ListTaskUpdateRequest,
)
from src.application.services.list_task_service import ListTasksUseCase


class TestListTasksUseCase:
    @pytest.fixture
    def list_task_service(self):
        mock_repo = MagicMock()
        return ListTasksUseCase(mock_repo)

    @pytest.fixture
    def list_task_request(self):
        return ListTaskRequest(title="Test List", description="Test Description")

    @pytest.fixture
    def list_task_response(self):
        return ListTaskResponse(
            id_list_task=1, title="Test List", description="Test Description", tasks=[]
        )

    def test_get_list_tasks_success(self, list_task_service, list_task_response):
        list_task_service.repo.get_list_tasks.return_value = [list_task_response]

        result = list_task_service.get_list_tasks()

        assert len(result) == 1
        assert result[0].title == list_task_response.title

    def test_create_list_task_success(
        self, list_task_service, list_task_request, list_task_response
    ):
        list_task_service.repo.create_list_task.return_value = list_task_response

        result = list_task_service.create_list_task(list_task_request)

        assert result == list_task_response
        list_task_service.repo.create_list_task.assert_called_once()

    def test_update_list_task_success(self, list_task_service, list_task_response):
        list_task_id = 1
        update_request = ListTaskUpdateRequest(title="Updated List")
        list_task_service.repo.update_list_task.return_value = list_task_response

        result = list_task_service.update_list_task(list_task_id, update_request)

        assert result == list_task_response
        list_task_service.repo.update_list_task.assert_called_once_with(
            list_task_id, update_request
        )

    def test_delete_list_task_success(self, list_task_service):
        list_task_id = 1
        list_task_service.repo.delete_list_task.return_value = None

        list_task_service.delete_list_task(list_task_id)

        list_task_service.repo.delete_list_task.assert_called_once_with(list_task_id)
