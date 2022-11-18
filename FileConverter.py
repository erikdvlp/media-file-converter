import os
import shutil

from dotenv import load_dotenv
from tqdm import tqdm

from exceptions import MissingEnvException, MissingEnvValueException


class FileConverter:
    def __init__(self) -> None:
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
        required_dirs = [self.output_dir, f'{self.output_dir}{os.sep}chunks']
        for required_dir in required_dirs:
            if not os.path.exists(required_dir):
                os.makedirs(required_dir)

    def get_input_files(self) -> None:
        print('Gathering input files...')
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
        print('Converting .media files to a viewable format...')
        iteration = 0
        for input_file in tqdm(self.input_files):
            iteration += 1
            self.convert_file(input_file, iteration)

    def combine_chunks(self) -> None:
        print('Combining video chunks...')
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
        print('Finished.')
