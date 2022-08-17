from databases import Database

from taskiq_collector.settings import settings

database = Database(str(settings.db_url))
