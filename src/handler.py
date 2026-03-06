from werkzeug.datastructures.file_storage import FileStorage
import requests as req
import faster_whisper
import yt_dlp
from datetime import datetime


def get_summarize(prompt: str, transcribe: str, model: str, OLLAMA_URL: str) -> str:
    OLLAMA_URL = OLLAMA_URL+"/api/generate"

    prompt = prompt+"\nText to summarize:\n"+transcribe

    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = req.post(OLLAMA_URL, json=data)
        response = response.json().get("response")
    except Exception as e:
        response = e

    return str(response)


def transcribe_video(path: str, stt_model: str) -> str:
    model = faster_whisper.WhisperModel(stt_model)
    segments, info = model.transcribe(path, beam_size=5)

    result = "\n".join([segment.text for segment in segments])

    return result


def work_with_data(is_data_from_link: bool, data: str | FileStorage, prompt: str, llm_model: str, stt_model: str, OLLAMA_URL: str) -> str:
    try:
        file_path = f'/tmp/SimS/{datetime.now().timestamp()}'
        file_path_with_extansion = file_path+'.mp3'


        if is_data_from_link:
            ydl_opts = {
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': file_path,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([data])
        else:
            data.save(file_path_with_extansion)

        print("Transcribing...")

        transcribe = transcribe_video(file_path_with_extansion, stt_model)

        print("Summarizing...")

        result = get_summarize(prompt, transcribe, llm_model, OLLAMA_URL)
    except Exception as e:
        result = e

    return str(result)

