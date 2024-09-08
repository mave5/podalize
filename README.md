# Podalize: Podcast Transcription and Analysis

This GitHub repository contains a Streamlit app that allows users to transcribe podcasts and video/audio content, and chat with the pod transcript. The app uses OpenAI's Whisper for transcription and Pyannote.audio for speaker diarization. Users have the option to manually enter speaker names for speaker segmentation. The app works with YouTube URLs, audio URLs, and MP3 files. 




## How to install

- Install [Anaconda](https://www.anaconda.com/)

- Clone/download this repo to your local machine. 

- Get a pyannote.adudio access token by following the instructions: 
[here](https://github.com/mave5/podalize/blob/main/configs.py)


- Launch anaconda prompt and navigate to the repo on your local machine

- Create a conda environment

```
conda create -n podalize python=3.9
```

- Activate the conda environment

```
$ conda activate podalize
```

- Install packages

```
pip install -r requirements.txt
```

- Run streamlit app

```
$ streamlit run podalize_app.py
```

## Tips
- You may need to install ffmpeg. Follow instructions here: https://github.com/openai/whisper
- You would need to install youtube downloader: https://github.com/yt-dlp/yt-dlp
- Install [Ollama](https://github.com/ollama/ollama) for chat options


## Usage
Either upload a .mp3 file or provide a YouTube/Podcast URL for transcription and analysis.


## Refrencess
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Ollama](https://github.com/ollama/ollama)
- [LLama-index](https://github.com/run-llama/llama_index)


## Contributions Welcome

