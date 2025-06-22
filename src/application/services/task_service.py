from typing import List

from src.api.modules.tasks.schema import (
    TaskFilterRequest,
    TaskRequest,
    TaskResponse,
    TaskUpdateIdUserRequest,
    TaskUpdateRequest,
    TaskUpdateStatusRequest,
)
from src.domain.interfaces.task_interface import ITaskRepository
from src.domain.models.task import Task
from src.infrastructure.services.resend.resend_service import send_email


class TaskUseCase:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def get_tasks(self) -> List[TaskResponse]:
        try:
            tasks = self.repo.get_tasks()
            return [TaskResponse.model_validate(task) for task in tasks]
        except Exception as e:
            raise e

    def create_task(self, task: TaskRequest) -> TaskResponse:
        try:
            task.status = task.status.value
            task.priority = task.priority.value
            task.completeness = task.completeness.value
            task = Task(**task.model_dump())
            return self.repo.create_task(task)
        except Exception as e:
            raise e

    def update_task(self, id_task: int, request: TaskUpdateRequest) -> TaskResponse:
        try:
            return self.repo.update_task(id_task, request)
        except Exception as e:
            raise e

    def delete_task(self, id_task: int):
        try:
            return self.repo.delete_task(id_task)
        except Exception as e:
            raise e

    def get_task_by_id(self, id_task: int) -> TaskResponse:
        try:
            return self.repo.get_task_by_id(id_task)
        except Exception as e:
            raise e

    def get_tasks_by_user_id(self, id_user: int) -> List[TaskResponse]:
        try:
            return self.repo.get_tasks_by_user_id(id_user)
        except Exception as e:
            raise e

    def get_tasks_by_list_task_id(self, id_list_task: int) -> List[TaskResponse]:
        try:
            return self.repo.get_tasks_by_list_task_id(id_list_task)
        except Exception as e:
            raise e

    def get_filtered_tasks_by_list_task_id(
        self, id_list_task: int, request: TaskFilterRequest
    ) -> List[TaskResponse]:
        try:
            return self.repo.get_filtered_tasks_by_list_task_id(id_list_task, request)
        except Exception as e:
            raise e

    def update_task_status(
        self, id_task: int, request: TaskUpdateStatusRequest
    ) -> TaskResponse:
        try:
            return self.repo.update_task_status(id_task, request)
        except Exception as e:
            raise e

    def update_task_id_user(
        self, id_task: int, request: TaskUpdateIdUserRequest, email: str
    ) -> TaskResponse:
        try:
            task_updated = self.repo.update_task_id_user(id_task, request)
            send_email(
                email,
                "Task updated",
                f"The task {task_updated.title} has been assigned to you, please check it out.",
            )
            return task_updated
        except Exception as e:
            raise e
