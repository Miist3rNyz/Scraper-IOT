import logging
import argparse

from controllers.import_controller import ImportController
from db.scraper_database import ScraperDatabase
from import_scheduler import ImportScheduler
from flask import Flask
from controllers.routes import api_bp  # Importez le Blueprint défini dans controllers/routes.py
from db.cve_collection import CveCollection



if __name__ == "__main__":
    cve_collection = CveCollection()
    app=Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')

    # Setup args parser
    parser = argparse.ArgumentParser()

    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    import_parser = parser.add_subparsers(dest="command")

    import_cmd = import_parser.add_parser("import", help="Import data from NVD")
    import_cmd.add_argument("--cves", action="store_true", help="Import CVEs")
    import_cmd.add_argument("--cpes", action="store_true", help="Import CPEs")
    import_cmd.add_argument("--start-index", action="store", type=int, default=0, help="Import all data")

    update_cmd = import_parser.add_parser("update", help="Update data from NVD")
    update_cmd.add_argument("--cves", action="store_true", help="Update CVEs")
    update_cmd.add_argument("--cpes", action="store_true", help="Update CPEs")

    run_cmd = import_parser.add_parser("run", help="Run the scheduler")
    start_cmd = import_parser.add_parser("start", help="Start Flask server")
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

    if args.debug:
        stream_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Test database connection
    db = ScraperDatabase()
    if not db.test_connection():
        logger.error("Database connection failed")
        exit(1)
    else:
        logger.info(f"Database connection successful: {db.name}")

    # Select command
    if args.command == "import":
        if args.cves:
            logger.info("Importing CVEs")
            ImportController().import_cves(args.start_index)
        elif args.cpes:
            logger.info("Importing CPEs")
            ImportController().import_cpes()
    elif args.command == "update":
        if args.cves:
            logger.info("Updating CVEs")
            ImportController().update_cves()
        elif args.cpes:
            logger.info("Updating CPEs")
            ImportController().update_cpes()
    elif args.command == "run":
        logger.info("Running the scheduler")
        ImportScheduler().schedule_importer()
    elif args.command == "start":
        logger.info("Start Flask server")
        app.run(host='0.0.0.0', port=5005)

    logger.info("Exiting...")
