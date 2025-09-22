import logging
from pythonjsonlogger import jsonlogger
class RequestFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("level", record.levelname)
        log_record.setdefault("logger", record.name)
def configure_logging(level: str = "INFO"):
    handler = logging.StreamHandler()
    formatter = RequestFormatter("%(level)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]
