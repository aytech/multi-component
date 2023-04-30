from PostgresStorage import PostgresStorage
from db.models import Log


class Logs:
    storage: PostgresStorage

    def get_archive_logs(self, from_log: int) -> list[Log]:
        if from_log is None:
            return []
        return self.storage.get_logs(from_log=from_log)

    def get_latest_logs(self, to_log: int) -> list[Log]:
        if to_log is None:
            return []
        return self.storage.get_logs(to_log=to_log)

    def get_logs_chunk(self):
        return self.storage.get_logs()

    def __init__(self, storage: PostgresStorage):
        self.storage = storage
