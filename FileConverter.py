import os
import shutil

from dotenv import load_dotenv
from tqdm import tqdm

from exceptions import (
    MissingEmptyInputDirException,
    MissingEnvException,
    MissingEnvValueException,
)


class FileConverter:
    def __init__(self, logger) -> None:
        self.logger = logger
        self.load_env()
        self.set_up_dirs()

    def load_env(self) -> None:
        if not os.path.exists('.env'):
            raise MissingEnvException
        load_dotenv()
        self.input_dir = os.getenv('INPUT_DIR')
        self.output_dir = os.getenv('OUTPUT_DIR')
        self.output_file_type = os.getenv('OUTPUT_FILE_TYPE')
        self.ffmpeg_options = os.getenv('FFMPEG_OPTIONS')
        if not self.input_dir or not self.output_dir or not self.output_file_type:
            raise MissingEnvValueException
        self.input_files: list[str] = []

    def set_up_dirs(self) -> None:
        if not os.path.exists(self.input_dir) or not os.listdir(self.input_dir):
            raise MissingEmptyInputDirException
        dirs_to_create = [self.output_dir, f'{self.output_dir}{os.sep}chunks']
        for dir_to_create in dirs_to_create:
            if not os.path.exists(dir_to_create):
                os.makedirs(dir_to_create)

    def get_input_files(self) -> None:
        self.logger.info('Gathering input files...')
        input_files = []
        for root, _dirs, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.media'):
                    input_files.append(f'{root}{os.sep}{file}')
        input_files.sort()
        self.input_files = input_files

    def convert_file(self, input_file: str, iteration: int) -> None:
        command = f'ffmpeg -i {input_file} {self.ffmpeg_options} {self.output_dir}{os.sep}chunks{os.sep}{iteration}.ts'
        os.system(command)

    def convert_files(self) -> None:
        self.logger.info('Converting .media files to a viewable format...')
        iteration = 0
        for input_file in tqdm(self.input_files):
            iteration += 1
            self.convert_file(input_file, iteration)

    def combine_chunks(self) -> None:
        self.logger.info('Combining video chunks...')
        chunks = os.listdir(f'{self.output_dir}{os.sep}chunks')
        for chunk in chunks:
            if '.media' not in chunk:
                chunks.remove(chunk)
        chunks.sort()
        concat_string = 'concat:'
        for chunk in chunks:
            concat_string += f'{self.output_dir}{os.sep}chunks{os.sep}{chunk}|'
        concat_string = concat_string[:-1]
        command = f'ffmpeg -i "{concat_string}" -c copy {self.output_dir}{os.sep}output{self.output_file_type} -nostats -loglevel 0'
        os.system(command)

    def clean_up(self) -> None:
        shutil.rmtree(f'{self.output_dir}{os.sep}chunks')

    def start(self) -> None:
        self.get_input_files()
        self.convert_files()
        self.combine_chunks()
        self.clean_up()
        self.logger.info('Finished.')
