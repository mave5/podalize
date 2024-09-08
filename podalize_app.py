#from DocumentGenerator import DocumentGenerator
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
from sys import platform
import yaml
import torch
from streamlit import session_state
from llms import ollama_chat, ollama_generate
import rags

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)

st.title('Podalize: podcast transcription and analysis')

if st.button("Reset Session"):
    st.session_state.clear()
    st.write("Session state reset!")

# devices
if "devices" not in session_state:
    session_state.num_cuda = torch.cuda.device_count()
    session_state.device0 = 'mps' if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else 'cpu'
    session_state.devices = (session_state.device0,) + tuple(range(0, session_state.num_cuda))
device = st.selectbox('Select Device', session_state.devices, index=0)


uploaded_file = st.file_uploader("Choose an audio", type=["mp3", "wav"])
youtube_url = st.text_input("Youtube/Podcast URL")

if "audio_path" not in session_state:
    if uploaded_file or youtube_url:
        st.spinner(text="In progress...")
        if uploaded_file:
            p2audio = os.path.join(path2audios, uploaded_file.name)
            if not os.path.exists(p2audio):
                with open(p2audio, "wb") as f:
                    f.write(uploaded_file.getvalue())
        else:
            #p2audio = youtube_downloader(youtube_url, path2audios)
            p2audio, audio_dir = download_audio_as_mp3(youtube_url, output_dir=path2audios)



        session_state.audio_dir = audio_dir
        session_state.audio_path = p2audio

if "audio_path" in session_state:
    # audio diarization
    num_speakers = st.selectbox(
        "Number of speakers",
        ("auto", 1, 2, 3, 4, 5, 6, 7, 8, 9), index=0)
    print(num_speakers)
    if st.button("Segment") and "diarization" not in session_state:
        diarization = get_diarization(session_state.audio_path,
                                      use_auth_token,
                                      device=device,
                                      num_speakers=num_speakers)
        session_state.labels = diarization.labels()
        session_state.diarization = diarization

    if "audio_array" not in session_state:
        p2audio = mp3wav(session_state.audio_path)
        session_state.audio_path_wav = p2audio
        y, sr = torchaudio.load(p2audio)
        session_state.audio_array = y
        session_state.audio_sr = sr
        if verbose:
            print(f"audio shape: {y.shape}, sample rate: {sr}")

if "diarization" in session_state:
    labels = session_state.labels
    sr = session_state.audio_sr
    with st.sidebar:
        speakers_dict = {}
        for ii, sp in enumerate(labels):
            speakers_dict[sp] = st.text_input(f'Speaker_{ii}', sp)
            if f"{sp}_audio_path" not in session_state:
                s, e, _ = get_larget_duration(session_state.diarization, sp)
                s1 = int(s*sr)
                e1 = int(e*sr)
                path2sp = f"{path2audios}/{sp}.wav"
                waveform = session_state.audio_array[:, s1:e1]
                torchaudio.save(path2sp, waveform, sr)
                session_state[f"{sp}_audio_path"] = path2sp
            st.audio(session_state[f"{sp}_audio_path"], format="audio/wav", start_time=0)

    if "segements" not in session_state:
        p2s = session_state.audio_path_wav.replace(".wav", "_diar.json")
        with open(p2s, "r") as f:
            segements = json.load(f)
        session_state.segements = segements
        segements_dict = {}
        for k, v in segements.items():
            k = [float(i) for i in k.split(",")]
            segements_dict[(k[0], k[1])] = v
        session_state.segements_dict = segements_dict

if "audio_path" in session_state:
    model_sizes = ['tiny', 'small', 'base', 'medium', 'large']
    model_size = st.selectbox(
        'Select Model Size',
        model_sizes, index=0)

    if st.button("Transcribe") and "transcript" not in session_state:
        result = get_transcript(model_size=model_size,
                            path2audio=session_state.audio_path_wav)
        session_state.transcript = result


if "transcript" in session_state and "diarization" in session_state:
    result = session_state.transcript
    segements_dict = session_state.segements_dict
    if "segmented_transcript" not in session_state:
        output = merge_tran_diar(result, segements_dict, speakers_dict)
        session_state.segmented_transcript = output
        session_state.segmented_transcript_path = session_state.audio_path_wav.replace(".wav", ".txt")

    st.subheader("Transcript")
    for sp in speakers_dict:
        session_state.segmented_transcript = session_state.segmented_transcript.replace(sp, speakers_dict[sp])
    with open(session_state.segmented_transcript_path, 'w') as fp:
        fp.write(session_state.segmented_transcript)
    st.text_area(label="transcript",
                 value=session_state.segmented_transcript,
                 label_visibility='hidden',
                 height=512)

    speakers = list(speakers_dict.keys())
    spoken_time, spoken_time_secs = get_spoken_time(result, speakers)

# ollama
if "ollama" not in session_state:
    try:
        os.system("ollama --version")
        ollama_exist = True
        os.system("ollama list")
    except:
        ollama_exist = False
    session_state.ollama = ollama_exist

# chat
if session_state.get("ollama", None) and "transcript" in session_state and "diarization" in session_state:
        if "ollama_chat" not in session_state:
            session_state.ollama_chat = rags.ChatWithPod(session_state.segmented_transcript_path)

        st.markdown("## Chat with podcast")
        llm_model = st.selectbox('LLM Model', ('llama3', 'llama2', 'mistral'), index=0)
        #user_input = st.text_area("Prompt", value="Summarize the following text:", height=10)
        user_input = st.chat_input("Say something")
        segmented_transcript = session_state.segmented_transcript
        #prompt_vars = {"query": user_input,
        #               "reference": segmented_transcript}
        #with open('prompt.yml', 'r') as file:
        #    yaml_data = yaml.safe_load(file).get("v1.0")
        #    yaml_content = yaml.dump(yaml_data)
        #    prompt = yaml_content.format(**prompt_vars)
            
        if user_input:
            #chat_output = ollama_chat(prompt, model=llm_model)
            chat_output = session_state.ollama_chat.query(user_input)
            print("-" * 50)
            print(chat_output)
            print("-"*50)
            st.markdown(chat_output)


# analyze
if "transcript" in session_state and "diarization" in session_state:
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


    pod_name = st.text_input("Enter Podcast Name", value=os.path.basename(session_state.audio_path))
    st.download_button('Download transcript', session_state.segmented_transcript[3:])


    # if st.button('Download PDF'):
    #     args = {'title': pod_name,
    #             'author': 'Created by Podalize',
    #             'path2logs': path2logs}
    #     rg = DocumentGenerator(**args)
    #
    #     for f in spoken_fig:
    #         rg.add_image(f, caption="Percentage of spoken time per speaker")
    #         rg.add_new_page()
    #
    #     for f in wc_figs:
    #         rg.add_image(f, caption="Word cloud per speaker")
    #         rg.add_new_page()
    #
    #     output = output[3:]
    #     rg.add_section("Transcript", output)
    #     if verbose is True:
    #         print(f"number of figures: {rg.fig_count}")
    #     path2pdf = f'{path2logs}/podalize_{pod_name}'
    #     # rg.doc.generate_pdf(path2pdf, clean_tex=False, compiler='pdfLaTeX')
    #     rg.doc.generate_pdf(path2pdf, clean_tex=False)
    #     if verbose is True:
    #         print("podalized!")






