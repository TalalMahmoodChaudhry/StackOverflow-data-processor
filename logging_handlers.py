import logging
import sys

LOG_FORMAT = "%(levelname) -0s %(asctime)s %(name) -10s %(funcName) -10s %(lineno) -5d: %(message){}s".format('')


def initialize_logging() -> None:
    stream_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[stream_handler])
