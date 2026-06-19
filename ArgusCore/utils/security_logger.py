import logging
import os

os.makedirs(
    "logs",
    exist_ok=True
)

security_logger = logging.getLogger(
    "security"
)

security_logger.setLevel(
    logging.INFO
)

handler = logging.FileHandler(
    "logs/security.log"
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

handler.setFormatter(
    formatter
)

if not security_logger.handlers:

    security_logger.addHandler(
        handler
    )