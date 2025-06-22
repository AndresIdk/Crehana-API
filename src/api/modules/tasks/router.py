from typing import List, Union

from fastapi import APIRouter, Depends

from src.api.dependencies.DI import (
    get_auth_repository_postgres,
    get_task_repository_postgres,
)
from src.api.dependencies.jwt import get_current_user
from src.api.modules.tasks.schema import (
    TaskFilterRequest,
    TaskRequest,
    TaskResponse,
    TaskUpdateIdUserRequest,
    TaskUpdateRequest,
    TaskUpdateStatusRequest,
)
from src.application.responses.api_responses import ApiResponse, ApiResponseError
from src.application.services.auth_service import AuthUseCase
from src.application.services.task_service import TaskUseCase
from src.domain.interfaces.auth_interface import IAuthRepository
from src.domain.interfaces.task_interface import ITaskRepository

tasks_router = APIRouter(
    prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_current_user)]
)


@tasks_router.get(
    "/",
    response_model=Union[ApiResponse[List[TaskResponse]], ApiResponseError],
    summary="Get all tasks",
)
def get_tasks(repo: ITaskRepository = Depends(get_task_repository_postgres)):
    try:
        usecase = TaskUseCase(repo)
        tasks = usecase.get_tasks()
        return ApiResponse(
            message="Tasks retrieved successfully", data=tasks, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.post(
    "/",
    response_model=Union[ApiResponse[TaskResponse], ApiResponseError],
    summary="Create a task for a list task",
)
def create_task(
    request: TaskRequest, repo: ITaskRepository = Depends(get_task_repository_postgres)
):
    try:
        usecase = TaskUseCase(repo)
        task = usecase.create_task(request)
        return ApiResponse(
            message="Task created successfully", data=task, status_code=201
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.put(
    "/{task_id}",
    response_model=Union[ApiResponse[TaskResponse], ApiResponseError],
    summary="Update a task",
)
def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    repo: ITaskRepository = Depends(get_task_repository_postgres),
):
    try:
        usecase = TaskUseCase(repo)
        task = usecase.update_task(task_id, request)
        return ApiResponse(
            message="Task updated successfully",
            data=TaskResponse.model_validate(task),
            status_code=200,
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.delete(
    "/{task_id}",
    response_model=Union[ApiResponse[None], ApiResponseError],
    summary="Delete a task",
)
def delete_task(
    task_id: int, repo: ITaskRepository = Depends(get_task_repository_postgres)
):
    try:
        usecase = TaskUseCase(repo)
        usecase.delete_task(task_id)
        return ApiResponse(
            message="Task deleted successfully", data=None, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.get(
    "/{task_id}",
    response_model=Union[ApiResponse[TaskResponse], ApiResponseError],
    summary="Get a task by id",
)
def get_task_by_id(
    task_id: int, repo: ITaskRepository = Depends(get_task_repository_postgres)
):
    try:
        usecase = TaskUseCase(repo)
        task = usecase.get_task_by_id(task_id)
        return ApiResponse(
            message="Task retrieved successfully", data=task, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.get(
    "/user/{user_id}",
    response_model=Union[ApiResponse[List[TaskResponse]], ApiResponseError],
    summary="Get all tasks by user id",
)
def get_tasks_by_user_id(
    user_id: int, repo: ITaskRepository = Depends(get_task_repository_postgres)
):
    try:
        usecase = TaskUseCase(repo)
        tasks = usecase.get_tasks_by_user_id(user_id)
        return ApiResponse(
            message="Tasks retrieved successfully", data=tasks, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.get(
    "/list/{id_list_task}",
    response_model=Union[ApiResponse[List[TaskResponse]], ApiResponseError],
    summary="Get all tasks by task list id",
)
def get_tasks_by_list_task_id(
    id_list_task: int, repo: ITaskRepository = Depends(get_task_repository_postgres)
):
    try:
        usecase = TaskUseCase(repo)
        tasks = usecase.get_tasks_by_list_task_id(id_list_task)
        return ApiResponse(
            message="Tasks retrieved successfully", data=tasks, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.post(
    "/list/{id_list_task}/filtered",
    response_model=Union[ApiResponse[List[TaskResponse]], ApiResponseError],
    summary="Get filtered tasks by task list id",
)
def get_filtered_tasks_by_list_task_id(
    id_list_task: int,
    request: TaskFilterRequest,
    repo: ITaskRepository = Depends(get_task_repository_postgres),
):
    try:
        usecase = TaskUseCase(repo)
        tasks = usecase.get_filtered_tasks_by_list_task_id(id_list_task, request)
        return ApiResponse(
            message="Tasks retrieved successfully", data=tasks, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.put(
    "/{task_id}/status",
    response_model=Union[ApiResponse[TaskResponse], ApiResponseError],
    summary="Update a task status",
)
def update_task_status(
    task_id: int,
    request: TaskUpdateStatusRequest,
    repo: ITaskRepository = Depends(get_task_repository_postgres),
):
    try:
        usecase = TaskUseCase(repo)
        task = usecase.update_task_status(task_id, request)
        return ApiResponse(
            message="Task status updated successfully", data=task, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@tasks_router.put(
    "/user/{task_id}",
    response_model=Union[ApiResponse[TaskResponse], ApiResponseError],
    summary="Assign a task to a user",
)
def update_task_id_user(
    task_id: int,
    request: TaskUpdateIdUserRequest,
    repo: ITaskRepository = Depends(get_task_repository_postgres),
    repo_auth: IAuthRepository = Depends(get_auth_repository_postgres),
):
    try:
        usecase = TaskUseCase(repo)
        usecase_auth = AuthUseCase(repo_auth)
        user = usecase_auth.get_user_by_id(request.id_user)

        task = usecase.update_task_id_user(task_id, request, user.email)

        return ApiResponse(
            message="Task id user updated successfully", data=task, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)
