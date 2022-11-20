import logging
from enum import Enum


class Colour(Enum):
    RESET = '\033[0m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'


class LogManager:
    def __init__(self) -> None:
        logging.basicConfig(level=50, format='%(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(10)

    def info(self, message: str) -> None:
        formatted_message = f'{Colour.GREEN.value}{message}{Colour.RESET.value}'
        self.logger.info(formatted_message)

    def error(self, message: str) -> None:
        formatted_message = f'{Colour.RED.value}{message}{Colour.RESET.value}'
        self.logger.error(formatted_message)
