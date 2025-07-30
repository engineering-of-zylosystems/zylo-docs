import logging

class NoZyloDocsLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.name == "uvicorn.access" and isinstance(record.args, tuple) and len(record.args) >= 3:
            path = record.args[2]
            if isinstance(path, str) and path.startswith("/zylo-docs"):
                return False
        return True

    def setup_logging(self):
        """uvicorn 로거에 필터를 적용합니다."""
        logging.getLogger("uvicorn.access").addFilter(NoZyloDocsLogFilter())
