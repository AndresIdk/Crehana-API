from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from src.api.modules.tasks.schema import TaskResponse
from src.application.enums.task_enums import TaskCompleteness, TaskPriority, TaskStatus


class ListTaskBase(BaseModel):
    title: Optional[str] = Field(None, example="List of tasks")
    description: Optional[str] = Field(None, example="Description of the list")


class ListTaskRequest(ListTaskBase):
    title: str = Field(..., example="List of tasks")
    description: str = Field(..., example="Description of the list")


class ListTaskUpdateRequest(ListTaskBase):
    pass


class ListTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_list_task: int = Field(..., example=1)
    title: str = Field(..., example="List of tasks")
    description: str = Field(..., example="Description of the list")
    tasks: List[TaskResponse] = Field(
        ...,
        example=[
            TaskResponse(
                id_task=1,
                title="Task 1",
                description="Description of the task",
                status=TaskStatus.pending,
                priority=TaskPriority.low,
                completeness=TaskCompleteness.not_started,
                id_list_task=1,
                id_user=1,
            )
        ],
    )
