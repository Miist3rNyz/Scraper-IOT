import logging

if __name__ == "__main__":
    print("Hello World")

    # Logging
    format = "[%(asctime)s] %(levelname)s: %(message)s"
    file = "logs/import.log"
    level = logging.INFO
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(format=format, filename=file, level=level, datefmt=datefmt)

