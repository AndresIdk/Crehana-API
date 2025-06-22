from typing import List

from sqlalchemy.orm import Session

from src.api.modules.list_tasks.schema import ListTaskResponse, ListTaskUpdateRequest
from src.domain.exceptions.common_exceptions import ListTaskNotFound
from src.domain.interfaces.list_task_interface import IListTaskRepository
from src.domain.models.list_task import ListTask


class ListTaskRepositoryPostgres(IListTaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_list_tasks(self) -> List[ListTask]:
        list_tasks = ListTask.get_all(self.db)
        if not list_tasks:
            raise ListTaskNotFound("No list tasks found")
        return [ListTaskResponse.model_validate(list_task) for list_task in list_tasks]

    def create_list_task(self, list_task: ListTask) -> ListTask:
        list_task.save(self.db)
        return ListTaskResponse.model_validate(list_task)

    def update_list_task(
        self, id_list_task: int, request: ListTaskUpdateRequest
    ) -> ListTaskResponse:
        list_task_db = ListTask.get_by_id(self.db, id_list_task)
        if not list_task_db:
            raise ListTaskNotFound(f"List task with id {id_list_task} not found")
        list_task_db.update(self.db, request.model_dump(exclude_unset=True))
        return ListTaskResponse.model_validate(list_task_db)

    def delete_list_task(self, id_list_task: int) -> None:
        list_task = ListTask.get_by_id(self.db, id_list_task)
        if not list_task:
            raise ListTaskNotFound(f"List task with id {id_list_task} not found")
        list_task.delete(self.db)

    def get_by_id(self, id_list_task: int) -> ListTask:
        return ListTask.get_by_id(self.db, id_list_task)
