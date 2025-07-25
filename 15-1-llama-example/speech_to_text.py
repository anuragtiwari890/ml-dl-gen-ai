import sounddevice as sd
import numpy as np
import whisper
import tempfile
import os
import soundfile as sf
import requests
import json
import pyttsx3  # <-- import pyttsx3 for speech

# Load Whisper model
whisper_model = whisper.load_model("turbo")

# Record audio from mic (5 seconds)
def record_audio(duration=5, fs=16000):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return recording.flatten()

# Save numpy array to .wav file
def save_wav(filename, data, fs=16000):
    sf.write(filename, data, fs)

# Transcribe with Whisper (set language to Hindi)
def speech_to_text(audio_array):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        save_wav(tmpfile.name, audio_array)
        result = whisper_model.transcribe(tmpfile.name)
        os.unlink(tmpfile.name)
        return result["text"]

# Query Ollama running LLaMA 3 locally
def query_ollama_stream(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        # "stream": False,
        "options": {
            "temperature": 0.8,
            # "top_k": 10,
            "max_tokens": 100
        }
    }

    with requests.post(url, json=payload, stream=True) as response:
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                try:
                    chunk = json.loads(data)
                    full_response += chunk.get('response', '')
                    if chunk.get('done', False):
                        break
                except json.JSONDecodeError:
                    # skip or handle malformed JSON line
                    pass
        return full_response

# New function: speak text aloud
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    audio_data = record_audio(duration=5)
    print("Transcribing speech...")
    text = speech_to_text(audio_data)
    print(f"You said: {text}")

    print("Generating LLaMA 3 response...")
    answer = query_ollama_stream(text)
    print(f"Ollama says: {answer}")

    # Speak the response
    speak_text(answer)
