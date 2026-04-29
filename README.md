# Music Source Separation

Веб-приложение для разделения аудио на дорожки (вокал, бас, ударные, другие) с помощью Demucs.

---

## ✨ Возможности

- Разделение на 4 stems: vocals, bass, drums, other
- Веб-интерфейс на React + Vite
- API на FastAPI с автоматической документацией
- Поддержка GPU (CUDA) для ускорения обработки

---

## 🚀 Быстрый старт

### Требования

| Программа | Версия | Зачем |
|-----------|--------|-------|
| **Python** | 3.10+ | Бэкенд |
| **Node.js** | 18+ (LTS) | Фронтенд (React/Vite) |
| **Git** | любая | Клонирование репозитория |
| **ffmpeg** | любой | Обработка аудио ([скачать](https://ffmpeg.org/download.html)) |

> **Windows**: При установке Python поставьте галочку ✅ **Add Python to PATH**.

---

### 🔹 Вариант 1: Через venv (универсальный)

```cmd
:: 1. Клонируйте репозиторий
git clone https://github.com/ekwizor/muscai.git
cd muscai

:: 2. Создайте виртуальное окружение
py -m venv venv

:: 3. Активируйте его
:: Windows CMD:
venv\Scripts\activate.bat
:: PowerShell:
venv\Scripts\Activate.ps1
:: macOS/Linux:
source venv/bin/activate

:: 4. Установите зависимости (с CUDA)
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121

:: 5. Установка Demucs без зависимостей

pip install --no-deps git+https://github.com/facebookresearch/demucs.git

:: 5. Установите зависимости фронтенда
cd audio-ui && npm install && cd ..

:: 6. Запуск backend
python main.py
- Сервер запустится на http://localhost:8000
- Документация API: http://localhost:8000/docs

:: 7. Запуск frontend
cd audio-ui && npm run dev
- Приложение откроется на http://localhost:5173

---

Спецификации ПК:
4060 8gb
16 gb VRAM
R5 5600

