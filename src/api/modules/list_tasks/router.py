from typing import List, Union

from fastapi import APIRouter, Depends

from src.api.dependencies.DI import get_list_task_repository_postgres
from src.api.dependencies.jwt import get_current_user
from src.api.modules.list_tasks.schema import (
    ListTaskRequest,
    ListTaskResponse,
    ListTaskUpdateRequest,
)
from src.application.responses.api_responses import ApiResponse, ApiResponseError
from src.application.services.list_task_service import ListTasksUseCase
from src.domain.interfaces.list_task_interface import IListTaskRepository

list_tasks_router = APIRouter(
    prefix="/list_tasks", tags=["List Tasks"], dependencies=[Depends(get_current_user)]
)


@list_tasks_router.get(
    "/",
    response_model=Union[ApiResponse[List[ListTaskResponse]], ApiResponseError],
    summary="Get all list tasks",
)
def get_list_tasks(
    repo: IListTaskRepository = Depends(get_list_task_repository_postgres),
):
    try:
        usecase = ListTasksUseCase(repo)
        list_tasks = usecase.get_list_tasks()
        return ApiResponse(
            message="List tasks retrieved successfully",
            data=list_tasks,
            status_code=200,
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@list_tasks_router.post(
    "/",
    response_model=Union[ApiResponse[ListTaskResponse], ApiResponseError],
    summary="Create a list task",
)
def create_list_task(
    request: ListTaskRequest,
    repo: IListTaskRepository = Depends(get_list_task_repository_postgres),
):
    try:
        usecase = ListTasksUseCase(repo)
        list_task = usecase.create_list_task(request)
        return ApiResponse(
            message="List task created successfully",
            data=ListTaskResponse.model_validate(list_task),
            status_code=200,
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@list_tasks_router.put(
    "/{id_list_task}",
    response_model=Union[ApiResponse[ListTaskResponse], ApiResponseError],
    summary="Update a list task",
)
def update_list_task(
    id_list_task: int,
    request: ListTaskUpdateRequest,
    repo: IListTaskRepository = Depends(get_list_task_repository_postgres),
):
    try:
        usecase = ListTasksUseCase(repo)
        list_task = usecase.update_list_task(id_list_task, request)
        return ApiResponse(
            message="List task updated successfully",
            data=ListTaskResponse.model_validate(list_task),
            status_code=200,
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)


@list_tasks_router.delete(
    "/{id_list_task}",
    response_model=Union[ApiResponse[None], ApiResponseError],
    summary="Delete a list task",
)
def delete_list_task(
    id_list_task: int,
    repo: IListTaskRepository = Depends(get_list_task_repository_postgres),
):
    try:
        usecase = ListTasksUseCase(repo)
        usecase.delete_list_task(id_list_task)
        return ApiResponse(
            message="List task deleted successfully", data=None, status_code=200
        )
    except Exception as e:
        return ApiResponseError(error=str(e), status_code=500)
