from myutils import *
import whisper
import time
import datetime
from pyannote.audio import Pipeline
import json
import os
import pickle
import matplotlib.pyplot as plt
from pytube import YouTube
from pathlib import Path
from pydub import AudioSegment
import streamlit as st
verbose = False

def yt_downloader(url, destination, bitrate="48k", verbose=True):
    video = YouTube(str(url))
    video = video.streams.filter(only_audio=True).first()
    title = video.title
    if verbose:
        print(f"downloading {title}")
    out_file = video.download(destination)
    _, ext = os.path.splitext(out_file)
    path2mp3 = out_file.replace(ext, ".mp3")
    if os.path.exists(path2mp3):
        return path2mp3
    audio_mp4 = AudioSegment.from_file(out_file, "mp4")
    audio_mp4.export(path2mp3, format="mp3", bitrate=bitrate)
    os.remove(out_file)
    if verbose:
        print(f"exported {os.path.basename(path2mp3)}")
    return path2mp3



def youtube_downloader(url, destination):
    path2mp3 = str(Path("./data/audio.mp3"))
    os.system(f'yt-dlp -x --audio-format mp3 -o {path2mp3} {url}')
    return path2mp3

def merge_tran_diar(result, segements_dict, speakers_dict):
    output = ""
    prev_sp = ""
    transcribed = set()
    for idx, seg in enumerate(result['segments']):
        if (idx in transcribed):
            continue
        seg = {k: v for k, v in seg.items() if k in ("start", "end", "text")}
        start = str(datetime.timedelta(seconds=round(seg['start'], 0)))
        if start.startswith('0'):
            start = start[2:]
        end = str(datetime.timedelta(seconds=round(seg['end'], 0)))
        if end.startswith('0'):
            end = end[2:]

        overlaps = {}
        for k, sp in segements_dict.items():
            if seg["start"] > k[1] or seg['end'] < k[0]:
                continue

            ov = getOverlap(k, (seg["start"], seg["end"]))
            if ov >= 0.3:
                overlaps[sp] = ov
                transcribed.add(idx)
        if overlaps:
            sp = max(overlaps, key=overlaps.get)
            result['segments'][idx]['speaker'] = sp
            ov = max(overlaps.values())
            if sp != prev_sp:
                out = "\n\n\n" + f"{sp}           {start}\n" + seg['text']
                # print(out)
                output += out
                # print("-"*50)
                # print(f"id: {idx}, {sp}\n")
                # print(f"[{start}, {end}]", seg['text'])
                prev_sp = sp
            else:
                prev_sp = sp
                out = seg['text']
                # print(out)
                output += out
                # print(f"[{start}, {end}]", seg['text'])
    result['speakers'] = list(set(segements_dict.values()))

    for sp in speakers_dict:
        output = output.replace(sp, speakers_dict[sp])
    return output

def get_segments(diarization, speaker_dict):
    segments_dict = {}
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start_end = f"{turn.start},{turn.end}"
        segments_dict[start_end] = speaker_dict.get(speaker, speaker)
    return segments_dict 

def get_larget_duration(diarization, speaker, max_length=5.0):
    maxsofar = -float('Inf')
    s, e, d = 0, 0, 0 
    for turn, _, sp in diarization.itertracks(yield_label=True):
        d = turn.end - turn.start
        if  d > maxsofar and sp==speaker:
            maxsofar = d
            s, e = turn.start, turn.end
    if verbose:
        print(speaker, f"start: {s:.1f}, end: {e:.1f}, duration: {maxsofar:.1f} secs")
    m = (s + e) / 2
    s = max(0, m - max_length/2)
    e = min(m + max_length/2, e)
    return s, e, maxsofar

def get_transcript(model_size, path2audio):
    # check if trainscript available
    _,ext = os.path.splitext(path2audio)
    p2f = path2audio.replace(ext, f"_{model_size}.json")
    if os.path.exists(p2f):
        with open(p2f, 'r') as f:
            result = json.load(f)
        return result
    
    if verbose:
        print("loading model ...")
    model = whisper.load_model(model_size)

    if verbose:
        print("transcribe ...")
    st = time.time()
    result = model.transcribe(path2audio)
    el = time.time() - st
    if verbose:
        print(f"elapsed time: {el:.2f} sec")
    
    # store transcript
    with open(p2f, "w") as f:
        json.dump(result,f)    
    
    return result


def merge_intervals(intervals_dict):
    intervals = list(intervals_dict.keys())
    speakers = list(intervals_dict.values())
    assert len(intervals) == len(speakers)
    
    sorted_intervals = intervals #sorted(intervals, key=lambda x: x[0])
    sorted_speakers = [[sp] for sp in speakers]
    
    interval_index = 0
    for  inv, sp in zip(sorted_intervals, sorted_speakers):

        if inv[0] > sorted_intervals[interval_index][1]:
            interval_index += 1
            sorted_intervals[interval_index] = inv
            sorted_speakers[interval_index] = sp
        else:
            sorted_intervals[interval_index] = [sorted_intervals[interval_index][0], inv[1]]
            sorted_speakers[interval_index].extend(sp) 
            
    intervals = sorted_intervals[:interval_index+1]
    speakers = sorted_speakers[:interval_index+1]
    assert len(intervals) == len(speakers)
    speakers = [list(set(sp)) for sp in speakers]
    
    intervals_dict = {(inv[0],inv[1]):sp for inv,sp in zip(intervals, speakers)}
    return intervals_dict

def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def mp3wav(p2mp3):
    if ".wav" in p2mp3:
        return p2mp3
    p2wav = p2mp3.replace(".mp3", ".wav")
    if os.path.exists(p2wav):
        return p2wav
        
    from pydub import AudioSegment
    if verbose:
        print(f"loading {p2mp3}")
    sound = AudioSegment.from_mp3(p2mp3)
    
    if verbose:
        print(f"exporting to {p2wav}")
    sound.export(p2wav, format="wav")
    return p2wav


def get_diarization(p2audio, use_auth_token):
    _, ext = os.path.splitext(p2audio)
    p2s = p2audio.replace(ext, "_diar.json")
    p2p = p2audio.replace(ext, "_diar.pkl")

    if os.path.exists(p2p):
        if verbose:
            print(f"loading {p2p}")
        with open(p2p, 'rb') as handle:
            diarization = pickle.load(handle)

        speaker_dict = {}
        segments_dict = get_segments(diarization, speaker_dict)
        with open(p2s, "w") as f:
            json.dump(segments_dict,f)
            if verbose:
                print(f"dumped diarization to {p2s}")

    else:
        p2audio = mp3wav(p2audio)
        if verbose:
            print("loading model ...")
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=use_auth_token)
        
        if verbose:
            print("diarization ...")
        diarization = pipeline(p2audio)    
        
        # save diarization
        with open(p2p, 'wb') as handle:
            pickle.dump(diarization, handle, protocol=pickle.HIGHEST_PROTOCOL)


        speaker_dict = {}
        segments_dict = get_segments(diarization, speaker_dict)
        with open(p2s, "w") as f:
            json.dump(segments_dict,f)
            if verbose:
                print(f"dumped diarization to {p2s}")

    return diarization


def get_spoken_time(result, speakers):
    spoken_time = {}
    spoken_time_secs = {}
    for sp in speakers:
        st = sum([seg['end']-seg['start'] for seg in result['segments'] if seg.get('speaker', None)==sp])
        spoken_time_secs[sp] = st    
        st = str(datetime.timedelta(seconds=round(st,0)))
        spoken_time[sp] = st
    return spoken_time, spoken_time_secs


def get_world_cloud(result, speakers_dict, path2figs="./data/logs"):
    from wordcloud import WordCloud
    speakers = result['speakers']
    figs = []
    for sp in speakers:
        words = ''.join([seg['text'] for seg in result['segments'] if seg.get('speaker')==sp])
        if words == '':
            continue
        wordcloud = WordCloud(max_font_size=40, background_color='white').generate(words)
        fig = plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title(speakers_dict[sp])
        plt.axis("off")
        st.pyplot(fig)
        
        p2f = f"{path2figs}/{speakers_dict[sp]}.png"
        figs.append(p2f)
        plt.savefig(p2f)    
    return figs

def get_audio_format(p2a, verbose=False):
    import magic
    with open(p2a, "rb") as f:
        audio_data = f.read()
    audio_format = magic.from_buffer(audio_data, mime=True)
    if verbose:
        print(f"The audio file is in the {audio_format} format.")
    return audio_format
def audio2wav(p2audio, verbose=False):
    if ".wav" in p2audio:
        if verbose:
            print("audio is in wav format!")
        return p2audio
    _, ext = os.path.splitext(p2audio)
    p2wav = p2audio.replace(ext, ".wav")
    if os.path.exists(p2wav):
        if verbose:
            print(f"{p2audio} exists!")
        return p2wav

    from pydub import AudioSegment
    if verbose:
        print(f"loading {p2audio}")
    sound = AudioSegment.from_file(p2audio)

    if verbose:
        print(f"exporting to {p2wav}")
    sound.export(p2wav, format="wav")
    return p2wav
