# Podalize: Podcast Transcription and Analysis

This GitHub repository contains a Streamlit app that allows users to transcribe podcasts and video/audio content, as well as perform text analysis on the transcript. The app uses OpenAI's Whisper for transcription and Pyannote.audio for speaker diarization. Users have the option to manually enter speaker names and the app works with YouTube URLs, audio URLs, and MP3 files. The app outputs spoken time, a word cloud per speaker, and a transcript of the audio, and the results can be downloaded as a PDF file.


[Sample episode](https://github.com/mave5/podalize/blob/main/data/podalize_Season%202%20Ep%2022%20Geoff%20Hinton%20on%20revolutionizing%20artificial%20intelligence%20again.pdf)

![usage](https://github.com/mave5/podalize/blob/main/data/usage.png)

## How to install

Note: This code was only tested on Ubuntu 20.04.5 LTS.

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

## Tips
- You may need to install ffmpeg. Follow instructions here: https://github.com/openai/whisper
- You would need to install youtube downloader: https://github.com/yt-dlp/yt-dlp


## Usage
Either upload a .mp3 file or provide a YouTube/Podcast URL for transcription and analysis.


## Refrencess
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [OpenAI Whisper](https://github.com/openai/whisper)


## Contributions Welcome

### TODo
- running the app on windows and macos
- dockerize 
