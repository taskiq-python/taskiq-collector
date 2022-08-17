from datetime import datetime

import ormar
from pydantic import Json

from taskiq_collector.db.base import BaseMeta
from taskiq_collector.db.fields import JsonDict, JsonList


class TaskModel(ormar.Model):  # type: ignore[no-redef]
    """Model for TaskiqMessage."""

    class Meta(BaseMeta):
        tablename = "taskiq_tasks"

    id: int = ormar.Integer(primary_key=True)
    created: datetime = ormar.DateTime(timezone=True, default=datetime.now)

    task_id: str = ormar.String(max_length=100, index=True)
    task_name: str = ormar.String(max_length=250, index=True)  # noqa: WPS432
    labels: Json = JsonDict()
    args: Json = JsonList()
    kwargs: Json = JsonDict()

    # If task were completed
    completed: bool = ormar.Boolean(default=False)

    # Result parameters
    is_err: bool = ormar.Boolean(nullable=True)
    log: str = ormar.Text(nullable=True)
    return_value: str = ormar.Text(nullable=True)
    execution_time: float = ormar.Float(nullable=True)
