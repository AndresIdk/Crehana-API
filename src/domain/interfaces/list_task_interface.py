from abc import ABC, abstractmethod
from typing import List

from src.domain.models.list_task import ListTask


class IListTaskRepository(ABC):
    @abstractmethod
    def get_list_tasks(self) -> List[ListTask]:
        pass

    @abstractmethod
    def create_list_task(self, list_task: ListTask) -> ListTask:
        pass

    @abstractmethod
    def update_list_task(self, id_list_task: int, list_task: ListTask) -> ListTask:
        pass

    @abstractmethod
    def delete_list_task(self, id_list_task: int) -> None:
        pass
