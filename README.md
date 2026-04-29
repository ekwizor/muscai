# Audio Stem Separator

Сервис для разделения музыкальных треков на составляющие — **vocals, drums, bass, other** — с помощью предобученной модели Demucs (архитектура htdemucs).  
Включает REST API на FastAPI и простой веб-интерфейс на React для прослушивания и скачивания стемов.

## Возможности

 - Загрузка аудиофайла (MP3/WAV) через веб-интерфейс и получение ZIP-архива со стемами  
 -  Скачивание каждого стема отдельно или полного архива  
 -  Прослушивание стемов прямо в браузере  
 -  Оценка качества разделения на тестовом наборе MUSDB18 (метрики SDR, SIR, SAR)  
 -  Jupyter Notebook с демонстрацией загрузки своего трека и анализом результата  

## Установка

###

```bash```
git clone https://github.com/ekwizor/muscai
cd muscai

### 2. Установите зависимости Python

pip install -r requirements.txt

```Для работы с GPU потребуется PyTorch с поддержкой CUDA.```

### 3. Frontend (React)

cd audio-ui
npm install

### Запуск

```FastAPI```
python main.py

Сервер стартует по адресу http://localhost:8000.
Документация API доступна интерактивно по /docs

```Frontend```

npm run dev

Приложение откроется по умолчанию на http://localhost:5173.
Убедитесь, что в файле App.jsx переменная API_URL указывает на работающий бэкенд (по умолчанию http://localhost:8000/separate).