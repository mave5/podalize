from pathlib import Path
import os


path2audios = str(Path("../data"))
path2logs = str(Path("../data/logs"))
os.makedirs(path2audios, exist_ok=True)
os.makedirs(path2logs, exist_ok=True)

# printing verbose
verbose = False

# pyannote.audio api access token
# visit hf.co/pyannote/speaker-diarization and hf.co/pyannote/segmentation and accept user conditions
# visit hf.co/settings/tokens to create an access token
# set use_auth_token using the token here or store it in a file named api.token to be loaded
with open("api.token") as f:
    use_auth_token = f.read()
