import json
import wave
from vosk import Model, KaldiRecognizer
from config import MODEL_PATH
from utils import save_temp_file, cleanup_temp_file
from schemas import ASRResponse

# Загрузка модели VOSK
model = Model(MODEL_PATH)


def transcribe_audio(file_path: str):
    with wave.open(file_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 44100]:
            raise ValueError("Аудиофайл должен быть моно с частотой дискретизации 8, 16 или 44.1 кГц")

        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                results.append(json.loads(recognizer.Result()))

        results.append(json.loads(recognizer.FinalResult()))
        return results


def analyze_raised_voice(words: list) -> bool:
    """Пример анализа голоса."""
    return any(word["conf"] < 0.5 for word in words)


async def process_audio(file) -> ASRResponse:
    temp_file = save_temp_file(file)
    try:
        recognition_results = transcribe_audio(temp_file)

        # Формируем ответ
        dialog = {"receiver": [], "transmitter": []}
        result_duration = {"receiver": 0, "transmitter": 0}
        roles = ["receiver", "transmitter"]

        for i, res in enumerate(recognition_results):
            if "text" in res and res["text"]:
                role = roles[i % 2]
                text = res["text"]
                duration = len(text) * 0.5  # Примерная длительность
                raised_voice = analyze_raised_voice(res.get("result", []))
                gender = "male" if "он" in text or "его" in text else "female"

                dialog[role].append({
                    "text": text,
                    "duration": duration,
                    "raised_voice": raised_voice,
                    "gender": gender
                })
                result_duration[role] += duration

        return ASRResponse(dialog=dialog, result_duration=result_duration)
    finally:
        cleanup_temp_file(temp_file)
