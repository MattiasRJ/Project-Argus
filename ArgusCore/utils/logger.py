import logging

from logging.handlers import TimedRotatingFileHandler

# =========================
# LOGGER MONITOR
# =========================

monitor_logger = logging.getLogger("monitor_logger")

monitor_handler = TimedRotatingFileHandler(
    "logs/monitor.log",
    when="midnight",
    interval=1,
    backupCount=7
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

monitor_handler.setFormatter(formatter)

monitor_logger.addHandler(monitor_handler)

monitor_logger.setLevel(logging.INFO)

# =========================
# LOGGER DETECTIONS
# =========================

detection_logger = logging.getLogger("detection_logger")

detection_handler = TimedRotatingFileHandler(
    "logs/detections.log",
    when="midnight",
    interval=1,
    backupCount=7
)

detection_handler.setFormatter(formatter)

detection_logger.addHandler(detection_handler)

detection_logger.setLevel(logging.INFO)

# =========================
# LOGGER ERRORS
# =========================

error_logger = logging.getLogger("error_logger")

error_handler = TimedRotatingFileHandler(
    "logs/errors.log",
    when="midnight",
    interval=1,
    backupCount=7
)

error_handler.setFormatter(formatter)

error_logger.addHandler(error_handler)

error_logger.setLevel(logging.ERROR)