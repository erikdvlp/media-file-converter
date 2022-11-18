# `.media` File Converter

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

Converts `.media` files created by wifi-enabled security cameras, such as those made by Littlelf and LARKKEY on Amazon, into a viewable format (e.g. `.mp4`).

This code handles the batch logic of gathering, ordering, and concatenating the thousands of files produced by these cameras. The video conversion itself is handled by FFmpeg.

## :rocket: Usage

### Pre-requisites

- [Python](https://www.python.org)
- [FFmpeg](https://ffmpeg.org)

### Run

1. Clone the repo.
2. Create an `.env` file in the project root and fill in the values from `.env.schema`.
3. Move `.media` files to be converted into your specified input directory.
4. Install dependencies (e.g. `pip install -r requirements.txt`).
5. Run `python run.py`.

### Space and time considerations

The application requires a considerable amount of storage space to run; roughly twice the original files' usage. Most of this space will be freed again once the application is finished running.

Converting large batches of files may take a considerable amount of time. Tweaking the FFmpeg settings in the `.env` file can speed up processing at the cost of video quality.
