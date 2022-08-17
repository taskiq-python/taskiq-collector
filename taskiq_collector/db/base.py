from ormar import ModelMeta

from taskiq_collector.db.config import database
from taskiq_collector.db.meta import meta


class BaseMeta(ModelMeta):
    """Base metadata for models."""

    database = database
    metadata = meta
