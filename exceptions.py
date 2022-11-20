class MissingEnvException(Exception):
    def __str__(self) -> str:
        return 'No .env file found. Create the file using format from .env.schema.'


class MissingEnvValueException(Exception):
    def __str__(self) -> str:
        return 'One or more values is missing from .env file. Follow the format from .env.schema.'


class MissingEmptyInputDirException(Exception):
    def __str__(self) -> str:
        return 'Specified input directory is missing or empty.'
