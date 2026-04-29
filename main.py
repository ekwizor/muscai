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

@app.post("/separate")
async def separate(file: UploadFile):
    # Читаем аудио в тензор
    data = await file.read()
    audio, sr = torchaudio.load(io.BytesIO(data))

    # Разделяем
    raw = separator.separate_tensor(audio, sr)
    stems = parse_demucs_output(raw)

    # Сохраняем стемы в ZIP прямо в памяти
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as zf:
        for name, tensor in stems.items():
            wav_buf = io.BytesIO()
            torchaudio.save(wav_buf, tensor.cpu(), sr, format="wav")
            zf.writestr(f"{name}.wav", wav_buf.getvalue())

    zip_buf.seek(0)
    return Response(zip_buf.read(), media_type="application/zip",
                    headers={"Content-Disposition": "attachment; filename=stems.zip"})

@app.get("/")
def root():
    return {"message": "Separator is running"}

# === Точка входа для запуска через python main.py ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)