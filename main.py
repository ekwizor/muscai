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

# Загружаем модель один раз при старте
device = "cuda" if torch.cuda.is_available() else "cpu"
separator = Separator(model="htdemucs", device=device)

def parse_demucs_output(raw):
    """Делает словарь из любого ответа Demucs"""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, tuple):
        d = next((x for x in raw if isinstance(x, dict)), None)
        if d:
            return d
        t = raw[0]
        names = ["vocals", "drums", "bass", "other"][:t.shape[0]]
        return {n: t[i] for i, n in enumerate(names)}
    return {"output": raw}


@app.get("/")
def root():
    return {"message": "Separator is running"}

# === Точка входа для запуска через python main.py ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)