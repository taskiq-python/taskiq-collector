from fastapi.routing import APIRouter

from taskiq_collector.web.api import docs, monitoring, tasks

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
