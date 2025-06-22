from abc import ABC, abstractmethod
from typing import List

from src.api.modules.tasks.schema import (
    TaskFilterRequest,
    TaskUpdateIdUserRequest,
    TaskUpdateRequest,
)
from src.domain.models.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    def get_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    def create_task(self, task: Task) -> Task:
        pass

    @abstractmethod
    def update_task(self, id_task: int, request: TaskUpdateRequest) -> Task:
        pass

    @abstractmethod
    def delete_task(self, id_task: int) -> None:
        pass

    @abstractmethod
    def get_task_by_id(self, id_task: int) -> Task | None:
        pass

    @abstractmethod
    def get_tasks_by_user_id(self, id_user: int) -> List[Task]:
        pass

    @abstractmethod
    def get_tasks_by_list_task_id(self, id_list_task: int) -> List[Task]:
        pass

    @abstractmethod
    def get_filtered_tasks_by_list_task_id(
        self, id_list_task: int, request: TaskFilterRequest
    ) -> List[Task]:
        pass

    @abstractmethod
    def update_task_status(self, id_task: int, request: TaskUpdateRequest) -> Task:
        pass

    @abstractmethod
    def update_task_id_user(
        self, id_task: int, request: TaskUpdateIdUserRequest
    ) -> Task:
        pass
