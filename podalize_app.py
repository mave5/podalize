from DocumentGenerator import DocumentGenerator
from myutils import *
import datetime
import json
import streamlit as st
import os
import subprocess
import matplotlib.pyplot as plt
import torchaudio
from glob import glob
from configs import *


st.title('Podalize: podcast transcription and analysis')
uploaded_file = st.file_uploader("Choose an audio", type=["mp3", "wav"])
youtube_url = st.text_input("Youtube/Podcast URL")

if uploaded_file or youtube_url:
    st.spinner(text="In progress...")
    if uploaded_file:
        p2audio = os.path.join(path2audios, uploaded_file.name)
        if not os.path.exists(p2audio):
            with open(p2audio, "wb") as f:
                f.write(uploaded_file.getvalue())
    if youtube_url:
        if "youtube.com" in youtube_url:
            p2audio = youtube_downloader(youtube_url, path2audios)
        else:
            path2out = os.path.join(path2audios, "audio.unknown")
            subprocess.run([f"youtube-dl", f"{youtube_url}", f"-o{path2out}"])
            p2audio = audio2wav(path2out)
            os.remove(path2out)



    # diarization
    diarization = get_diarization(p2audio, use_auth_token)
    p2audio = mp3wav(p2audio)
    labels = diarization.labels()
    if verbose:
        print(f"speakers: {labels}")
    y, sr = torchaudio.load(p2audio)
    if verbose:
        print(f"audio shape: {y.shape}, sample rate: {sr}")

    with st.sidebar:
        speakers_dict = {}
        for ii, sp in enumerate(labels):
            speakers_dict[sp] = st.text_input(f'Speaker_{ii}', sp)
            s, e, _ = get_larget_duration(diarization, sp)
            s1 = int(s*sr)
            e1 = int(e*sr)
            path2sp = f"{path2audios}/{sp}.wav"
            waveform = y[:, s1:e1]
            torchaudio.save(path2sp, waveform, sr)
            st.audio(path2sp, format="audio/wav", start_time=0)

    model_sizes = ['tiny', 'small', 'base', 'medium', 'large']
    model_size = st.selectbox(
        'Select Model Size',
        model_sizes, index=3)

    result = get_transcript(model_size=model_size,
                            path2audio=p2audio)
    
    p2s = p2audio.replace(".wav", "_diar.json")
    with open(p2s, "r") as f:
        segements = json.load(f)

    segements_dict = {}
    for k,v in segements.items():
        k = [float(i) for i in k.split(",")]
        segements_dict[(k[0], k[1])] = v

    output = merge_tran_diar(result, segements_dict, speakers_dict)
    st.subheader("Transcript")
    st.text_area(label="transcript", value=output, label_visibility='hidden', height=512)

    speakers = list(speakers_dict.keys())
    spoken_time, spoken_time_secs = get_spoken_time(result, speakers)

    st.header("Analyze")
    st.subheader("Spoken Time")
    labels = list(speakers_dict.values())
    sizes = spoken_time_secs.values()
    sizes_str = [str(datetime.timedelta(seconds=round(s, 0))) for s in sizes]
    labels = [f"{l},\n{z}" for l, z in zip(labels, sizes_str)]
    explode = (0.05,)*len(labels)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    fig1.savefig(f"{path2logs}/spoken_time.png")
    st.pyplot(fig1)


    # word cloud
    _ = get_world_cloud(result, speakers_dict)

    # list of figures
    spoken_fig = glob(path2logs + "/spoken*.png")
    all_figs = glob(path2logs + "/*.png")
    wc_figs = [f for f in all_figs if [v for v in speakers_dict.values() if v in f]]


    pod_name = st.text_input("Enter Podcast Name", value=os.path.basename(p2audio))
    if st.button('Download'):
        args = {'title': pod_name,
                'author': 'Created by Podalize',
                'path2logs': path2logs}
        rg = DocumentGenerator(**args)

        for f in spoken_fig:
            rg.add_image(f, caption="Percentage of spoken time per speaker")
            rg.add_new_page()

        for f in wc_figs:
            rg.add_image(f, caption="Word cloud per speaker")
            rg.add_new_page()

        output = output[3:]
        rg.add_section("Transcript", output)
        if verbose is True:
            print(f"number of figures: {rg.fig_count}")
        path2pdf = f'{path2logs}/podalize_{pod_name}'
        # rg.doc.generate_pdf(path2pdf, clean_tex=False, compiler='pdfLaTeX')
        rg.doc.generate_pdf(path2pdf, clean_tex=False)
        if verbose is True:
            print("podalized!")





