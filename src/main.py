from fastapi import FastAPI

from src.api.modules.auth.router import auth_router
from src.api.modules.list_tasks.router import list_tasks_router
from src.api.modules.tasks.router import tasks_router
from src.infrastructure.docs.swagger_config import custom_openapi

app = FastAPI()

app.openapi = lambda: custom_openapi(app)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(list_tasks_router)
# test comment
