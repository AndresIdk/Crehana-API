from typing import List

from src.api.modules.list_tasks.schema import (
    ListTaskRequest,
    ListTaskResponse,
    ListTaskUpdateRequest,
)
from src.domain.interfaces.list_task_interface import IListTaskRepository
from src.domain.models.list_task import ListTask


class ListTasksUseCase:
    def __init__(self, repo: IListTaskRepository):
        self.repo = repo

    def get_list_tasks(self) -> List[ListTaskResponse]:
        try:
            list_tasks = self.repo.get_list_tasks()
            return [
                ListTaskResponse.model_validate(list_task) for list_task in list_tasks
            ]
        except Exception as e:
            raise e

    def create_list_task(self, request: ListTaskRequest) -> ListTaskResponse:
        try:
            list_task = ListTask(**request.model_dump())
            return self.repo.create_list_task(list_task)
        except Exception as e:
            raise e

    def update_list_task(
        self, id_list_task: int, request: ListTaskUpdateRequest
    ) -> ListTaskResponse:
        try:
            return self.repo.update_list_task(id_list_task, request)
        except Exception as e:
            raise e

    def delete_list_task(self, id_list_task: int) -> None:
        try:
            return self.repo.delete_list_task(id_list_task)
        except Exception as e:
            raise e
