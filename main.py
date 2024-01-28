import logging

if __name__ == "__main__":
    print("Hello World")

    # Logging
    format = "[%(asctime)s] %(levelname)s: %(message)s"
    file = "logs/import.log"
    level = logging.INFO
    datefmt = "%Y-%m-%d %H:%M:%S"

    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(file)
    handler.setLevel(level)
    formatter = logging.Formatter(format, datefmt=datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    

