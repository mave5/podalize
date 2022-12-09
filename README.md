# Podalize: Podcast Transcription and Analysis
Streamlit app for podcast and audio content transcription and analysis using Pyannote.audio and OpenAI's Whisper. 

It works with .mp3 files or Youtube/Podcast URLs.

[Sample episode](https://github.com/mave5/podalize/blob/main/data/podalize_Season%202%20Ep%2022%20Geoff%20Hinton%20on%20revolutionizing%20artificial%20intelligence%20again.pdf)

![usage](https://github.com/mave5/podalize/blob/main/data/usage.png)

## How to install

Note: This code only was tested on Ubuntu 20.04.5 LTS.

- Install [Anaconda](https://www.anaconda.com/)

- Clone/download this repo to your local machine. 

- Get a pyannote.adudio access token by following the instructions: 
[here](https://github.com/mave5/podalize/blob/main/configs.py)


- Launch anaconda prompt and navigate to the repo on your local machine

- Create a conda environment from environment.yml

```
$ conda env create -f environment.yml
```

- Activate the conda environment

```
$ conda activate podalize
```

- Run streamlit app

```
$ streamlit run podalize_app.py
```

- Either upload a mp3 file or provide a YouTube/Podcast URL for transcription and analysis.

- You may need to install ffmpeg. Follow instructions here: https://github.com/openai/whisper

## Refrencess
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [OpenAI Whisper](https://github.com/openai/whisper)


