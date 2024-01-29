import logging

if __name__ == "__main__":
    print("Hello World")

    # Logging
    log_format = "[%(asctime)s] %(levelname)s: %(message)s"
    log_file = "logs/import.log"
    log_level = logging.INFO
    date_format = "%Y-%m-%d %H:%M:%S"

    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    formatter = logging.Formatter(log_format, datefmt=date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
