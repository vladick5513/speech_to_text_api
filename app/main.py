from fastapi import FastAPI, UploadFile, HTTPException
from schemas import ASRResponse
from asr import process_audio

app = FastAPI()


@app.post("/asr", response_model=ASRResponse)
async def asr(file: UploadFile):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Только MP3 файлы поддерживаются")
    return await process_audio(file)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)