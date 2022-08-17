from pydantic import BaseModel
from typing_extensions import TypeAlias

from taskiq_collector.db.models.task import TaskModel

UpdateModel: TypeAlias = TaskModel.get_pydantic(  # type: ignore
    exclude={
        "id",
        "task_id",
        "task_name",
        "args",
        "kwargs",
        "labels",
    },
)


class SearchResult(BaseModel):
    """Response for search request."""

    has_next: bool
    results: list[TaskModel]
