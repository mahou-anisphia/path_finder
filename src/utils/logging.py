import logging
from datetime import datetime


def setup_logging(log_filename="pathfinderlog-" + str(datetime.now())+".log"):
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    handler = logging.FileHandler(log_filename)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels of logs
    logger.addHandler(handler)

    return log_filename
