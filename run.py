from FileConverter import FileConverter
from LogManager import LogManager

logger = LogManager()
try:
    fc = FileConverter(logger)
    fc.start()
except Exception as e:
    logger.error(e)
