# Podalize: Podcast Transcription and Analysis
Streamlit app for podcast transcription and analysis using Pyannote.audio and OpenAI's Whisper. 

It works with .mp3 files or Youtube URLs.


## How to install

1- Install [Anaconda](https://www.anaconda.com/)

2- Clone/download this repo to your local machine. 

Get a pyannote.adudio access token by following the instructions 
[here](https://github.com/mave5/podalize/blob/main/configs.py)


3- Lanch anaconda prompt and navigate to the repo on your local machine

4- Create a conda environment from environment.yml

```
$ conda env create -f environment.yml
```

4- Activate the conda environment

```
$ conda activate podalize
```

5- Run streamlit app

```
$ streamlit run podalize_app.py
```

6- Either upload a mp3 file or provide a YouTube URL for transcription and analysis.

Note: only tested on Ubuntu. 

## Refrencess
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [OpenAI Whisper](https://github.com/openai/whisper)


