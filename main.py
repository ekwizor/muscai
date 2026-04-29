import io
import zipfile

from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import torch
import torchaudio
from fastapi.responses import Response
from demucs.api import Separator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на время тестов – любые origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Separator is running"}

# === Точка входа для запуска через python main.py ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)