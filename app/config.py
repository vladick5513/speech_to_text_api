import os

MODEL_PATH = "model"

# Проверка существования модели
if not os.path.exists(MODEL_PATH):
    raise Exception("Скачайте и разархивируйте VOSK модель в папку 'model'")