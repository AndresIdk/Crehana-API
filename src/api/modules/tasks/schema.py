from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.application.enums.task_enums import TaskCompleteness, TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="Task 1", min_length=1, max_length=255)
    description: Optional[str] = Field(
        None, example="Description of the task", min_length=1, max_length=255
    )
    status: Optional[TaskStatus] = Field(None, example=TaskStatus.pending)
    priority: Optional[TaskPriority] = Field(None, example=TaskPriority.low)
    completeness: Optional[TaskCompleteness] = Field(
        None, example=TaskCompleteness.not_started
    )
    id_list_task: Optional[int] = Field(None, example=1)


class TaskRequest(TaskBase):
    title: str = Field(..., example="Task 1", min_length=1, max_length=255)
    description: str = Field(
        ..., example="Description of the task", min_length=1, max_length=255
    )
    status: TaskStatus = Field(..., example=TaskStatus.pending)
    priority: TaskPriority = Field(..., example=TaskPriority.low)
    completeness: TaskCompleteness = Field(..., example=TaskCompleteness.not_started)
    id_list_task: int = Field(..., example=1)


class TaskUpdateRequest(TaskBase):
    pass


class TaskUpdateStatusRequest(BaseModel):
    status: TaskStatus = Field(..., example=TaskStatus.pending)


class TaskFilterRequest(BaseModel):
    status: Optional[TaskStatus] = Field(None, example=TaskStatus.pending)
    priority: Optional[TaskPriority] = Field(None, example=TaskPriority.low)
    completeness: Optional[TaskCompleteness] = Field(
        None, example=TaskCompleteness.not_started
    )


class TaskUpdateIdUserRequest(BaseModel):
    id_user: int = Field(..., example=1)


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_task: int = Field(..., example=1)
    title: str = Field(..., example="Task 1")
    description: str = Field(..., example="Description of the task")
    status: Optional[TaskStatus] = Field(None, example=TaskStatus.pending)
    priority: Optional[TaskPriority] = Field(None, example=TaskPriority.low)
    completeness: Optional[TaskCompleteness] = Field(
        None, example=TaskCompleteness.not_started
    )
    id_list_task: int = Field(..., example=1)
    id_user: Optional[int] = Field(None, example=1)
