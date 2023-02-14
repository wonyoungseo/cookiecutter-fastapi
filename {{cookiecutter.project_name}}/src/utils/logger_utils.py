import os
import logging
import sys
from loguru import logger

JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging(log_level="INFO"):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level)

    # remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "format": '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<magenta>{function}</magenta>:<cyan>{line}</cyan> // <level>{message}</level>',
                "serialize": JSON_LOGS
            },
            {
                "sink": "./logs/{time}.log",
                "format": '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<magenta>{function}</magenta>:<cyan>{line}</cyan> // <level>{message}</level>',
                "serialize": JSON_LOGS,
                "mode": "w+",
                "rotation": "00:00",
                "retention": "2 months"
            }
        ]
    )