import logging
import argparse

from controllers.import_controller import ImportController
from db.scraper_database import ScraperDatabase

if __name__ == "__main__":

    # Setup args parser
    parser = argparse.ArgumentParser()

    import_parser = parser.add_subparsers(dest="command")
    import_cmd = import_parser.add_parser("import", help="Import data from NVD")
    import_cmd.add_argument("--cves", action="store_true", help="Import CVEs")
    import_cmd.add_argument("--cpes", action="store_true", help="Import CPEs")

    args = parser.parse_args()

    # Setup logging
    log_format = "[%(asctime)s] %(levelname)s: %(message)s"
    log_file = "logs/import.log"
    date_format = "%Y-%m-%d %H:%M:%S"

    logger = logging.getLogger("scraper-iot")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format, datefmt=date_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Test database connection
    if not ScraperDatabase().test_connection():
        logger.error("Database connection failed")
        exit(1)

    # Select command
    if args.command == "import":
        if args.cves:
            logger.info("Importing CVEs")
            ImportController().import_cves()
        elif args.cpes:
            logger.info("Importing CPEs")
            ImportController().import_cpes()
