# Podalize: Podcast Transcription and Analysis
Streamlit app for podcast and audio content transcription and analysis using Pyannote.audio and OpenAI's Whisper. 

It works with .mp3 files or Youtube URLs.

[Sample episode](https://github.com/mave5/podalize/blob/main/data/podalize_Season%202%20Ep%2022%20Geoff%20Hinton%20on%20revolutionizing%20artificial%20intelligence%20again.pdf)

![usage](https://github.com/mave5/podalize/blob/main/data/usage.png)

## How to install

Note: This code only was tested on Ubuntu 20.04.5 LTS.

1- Install [Anaconda](https://www.anaconda.com/)

2- Clone/download this repo to your local machine. 

3- Get a pyannote.adudio access token by following the instructions: 
[here](https://github.com/mave5/podalize/blob/main/configs.py)


3- Launch anaconda prompt and navigate to the repo on your local machine

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

7- You may need to install ffmpeg. Follow instructions here: https://github.com/openai/whisper

## Refrencess
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [OpenAI Whisper](https://github.com/openai/whisper)


