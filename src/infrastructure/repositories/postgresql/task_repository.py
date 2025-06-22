from typing import List

from sqlalchemy.orm import Session

from src.api.modules.tasks.schema import (
    TaskFilterRequest,
    TaskResponse,
    TaskUpdateIdUserRequest,
    TaskUpdateRequest,
    TaskUpdateStatusRequest,
)
from src.domain.exceptions.common_exceptions import TaskNotFound
from src.domain.interfaces.task_interface import ITaskRepository
from src.domain.models.task import Task


class TaskRepositoryPostgres(ITaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_tasks(self) -> List[Task]:
        tasks = Task.get_all(self.db)
        if not tasks:
            raise TaskNotFound("No tasks found")
        return tasks

    def create_task(self, task: Task) -> Task:
        task.save(self.db)
        return TaskResponse.model_validate(task)

    def update_task(self, id_task: int, request: TaskUpdateRequest) -> Task:
        task_db = Task.get_by_id(self.db, id_task)
        if not task_db:
            raise TaskNotFound(f"Task with id {id_task} not found")

        update_data = request.model_dump(exclude_unset=True)
        task_db.update(self.db, update_data)

        return TaskResponse.model_validate(task_db)

    def delete_task(self, id_task: int) -> None:
        task = Task.get_by_id(self.db, id_task)
        if not task:
            raise TaskNotFound(f"Task with id {id_task} not found")
        task.delete(self.db)

    def get_task_by_id(self, id_task: int) -> Task:
        task = Task.get_by_id(self.db, id_task)
        if not task:
            raise TaskNotFound(f"Task with id {id_task} not found")
        return TaskResponse.model_validate(task)

    def get_tasks_by_user_id(self, id_user: int) -> List[Task]:
        tasks = Task.get_by_user_id(self.db, id_user)
        if not tasks:
            raise TaskNotFound(f"No tasks found for user with id {id_user}")
        return [TaskResponse.model_validate(task) for task in tasks]

    def get_tasks_by_list_task_id(self, id_list_task: int) -> List[Task]:
        tasks = Task.get_by_list_task_id(self.db, id_list_task)
        if not tasks:
            raise TaskNotFound(f"No tasks found for task list with id {id_list_task}")
        return [TaskResponse.model_validate(task) for task in tasks]

    def get_filtered_tasks_by_list_task_id(
        self, id_list_task: int, request: TaskFilterRequest
    ) -> List[Task]:
        tasks = self.db.query(Task).filter(Task.id_list_task == id_list_task)
        if request.status:
            tasks = tasks.filter(Task.status == request.status.value)
        if request.priority:
            tasks = tasks.filter(Task.priority == request.priority.value)
        if request.completeness:
            tasks = tasks.filter(Task.completeness == request.completeness.value)

        filtered_tasks = tasks.all()

        if not filtered_tasks:
            raise TaskNotFound(
                f"No tasks found for task list with id {id_list_task} with the filters: {request}"
            )

        return [TaskResponse.model_validate(task) for task in filtered_tasks]

    def update_task_status(
        self, id_task: int, request: TaskUpdateStatusRequest
    ) -> Task:
        task = Task.get_by_id(self.db, id_task)
        if not task:
            raise TaskNotFound(f"Task with id {id_task} not found")

        update_data = request.model_dump(exclude_unset=True)
        task.update(self.db, update_data)

        return TaskResponse.model_validate(task)

    def update_task_id_user(
        self, id_task: int, request: TaskUpdateIdUserRequest
    ) -> Task:
        task = Task.get_by_id(self.db, id_task)
        if not task:
            raise TaskNotFound(f"Task with id {id_task} not found")

        update_data = request.model_dump(exclude_unset=True)
        task.update(self.db, update_data)
        return TaskResponse.model_validate(task)
