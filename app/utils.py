import tempfile
import os
from pydub import AudioSegment


def save_temp_file(file) -> str:
    """Сохраняет файл в временную директорию и конвертирует в WAV."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        tmp_wav_name = tmp_wav.name

    audio = AudioSegment.from_file(file.file, format="mp3")
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(tmp_wav_name, format="wav")

    return tmp_wav_name


def cleanup_temp_file(file_path: str):
    """Удаляет временный файл."""
    if os.path.exists(file_path):
        os.remove(file_path)
