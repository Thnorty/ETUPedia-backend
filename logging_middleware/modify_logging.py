import datetime
import logging


class AddTimestamp(logging.Filter):
    def filter(self, record):
        record.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return True


class AddSeverity(logging.Filter):
    def filter(self, record):
        record.severity = record.levelname
        return True


class RemoveTaskName(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'taskName'):
            del record.taskName
        return True
