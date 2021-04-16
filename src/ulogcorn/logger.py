import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class UnifyHandler:

    def __init__(self, level=logging.DEBUG, modules=None) -> None:
        if modules is None:
            modules = [
                *logging.root.manager.loggerDict.keys(),  # noqa
                "gunicorn",
                "gunicorn.access",
                "gunicorn.error",
                "gunicorn.wsgi",
                "uvicorn",
                "uvicorn.access",
                "uvicorn.error",
                "uvicorn.asgi"
            ]
        self.level = level
        self.modules = modules
        self.handler = InterceptHandler()

    def setup(self):
        logging.root.setLevel(self.level)
        seen = set()
        for name in self.modules:
            if name not in seen:
                seen.add(name.split(".")[0])
                logging.getLogger(name).handlers = [self.handler]

        logger.configure(handlers=[{"sink": sys.stdout}])
