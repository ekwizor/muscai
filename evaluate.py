
import numpy as np
import pandas as pd
import torch
from demucs.api import Separator
import musdb
import mir_eval
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

mus = musdb.DB(root="./muscdb", subsets="test", is_wav=False)

tracks = mus[:]
print(f"Обрабатывается треков: {len(tracks)}")

# Модель
device = "cuda" if torch.cuda.is_available() else "cpu"
separator = Separator(model="htdemucs", device=device)

def parse_demucs_output(raw):
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

rows = []

for track in tracks:
    print(f"\nОбрабатываю: {track.name}")

    # Микс (channels, samples)
    mixture = torch.from_numpy(track.audio.T).float()
    raw_result = separator.separate_tensor(mixture, track.rate)
    stems = parse_demucs_output(raw_result)

    for stem_name in ["vocals", "drums", "bass", "other"]:
        if stem_name not in track.targets or stem_name not in stems:
            continue

        # Моно (усреднение каналов)
        ref = track.targets[stem_name].audio.T.mean(axis=0)
        est = stems[stem_name].detach().cpu().numpy().mean(axis=0)

        # Выравниваем длину
        min_len = min(len(ref), len(est))
        if min_len < track.rate * 0.5:
            continue
        ref = ref[:min_len]
        est = est[:min_len]

        # mir_eval принимает двумерные массивы (1, samples)
        sdr, sir, sar, _ = mir_eval.separation.bss_eval_sources(
            ref.reshape(1, -1),
            est.reshape(1, -1),
            compute_permutation=False
        )

        rows.append({
            "track": track.name,
            "stem": stem_name,
            "SDR": sdr[0],
            "SIR": sir[0],
            "SAR": sar[0]
        })

df = pd.DataFrame(rows)
if df.empty:
    print("\n❌ Нет данных. Проверьте датасет.")
else:
    avg_df = df.groupby("stem")[["SDR", "SIR", "SAR"]].mean().round(2)

    print("\n=== СРЕДНИЕ МЕТРИКИ ПО СТЕМАМ ===")
    print(avg_df)
    print("\nОбщее среднее:")
    print(avg_df.mean())

    # График
    ax = avg_df.plot(kind="bar", y=["SDR", "SIR", "SAR"], figsize=(8, 5))
    ax.set_title("Качество разделения Demucs (MUSDB18, 7 треков)")
    ax.set_ylabel("дБ")
    ax.grid(axis="y")
    plt.tight_layout()
    plt.savefig("metrics_bars.png")
    print("\nГрафик сохранён в metrics_bars.png")