from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.interfaces.auth_interface import IAuthRepository
from src.domain.interfaces.list_task_interface import IListTaskRepository
from src.domain.interfaces.task_interface import ITaskRepository
from src.infrastructure.data.db import get_db
from src.infrastructure.repositories.postgresql.auth_repository import (
    AuthRepositoryPostgres,
)
from src.infrastructure.repositories.postgresql.list_task_repository import (
    ListTaskRepositoryPostgres,
)
from src.infrastructure.repositories.postgresql.task_repository import (
    TaskRepositoryPostgres,
)


def get_auth_repository_postgres(db: Session = Depends(get_db)) -> IAuthRepository:
    return AuthRepositoryPostgres(db)


def get_task_repository_postgres(db: Session = Depends(get_db)) -> ITaskRepository:
    return TaskRepositoryPostgres(db)


def get_list_task_repository_postgres(
    db: Session = Depends(get_db),
) -> IListTaskRepository:
    return ListTaskRepositoryPostgres(db)
