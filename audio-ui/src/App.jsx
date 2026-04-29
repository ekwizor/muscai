import { useState } from 'react'
import JSZip from 'jszip'

import './App.css'

const API_URL = 'http://localhost:8000/separate'

function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [stems, setStems] = useState([])
  const [zipUrl, setZipUrl] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => setFile(e.target.files[0])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return

    setLoading(true)
    setError(null)
    setStems([])
    setZipUrl(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(API_URL, { method: 'POST', body: formData })
      if (!res.ok) throw new Error('Ошибка сервера')

      const blob = await res.blob()
      // Ссылка на скачивание всего ZIP
      setZipUrl(URL.createObjectURL(blob))

      // Распаковываем ZIP
      const zip = await JSZip.loadAsync(blob)
      const extracted = []

      for (const name of Object.keys(zip.files)) {
        if (!zip.files[name].dir && name.endsWith('.wav')) {
          const audioBlob = await zip.files[name].async('blob')
          extracted.push({
            name: name.replace('.wav', ''),
            url: URL.createObjectURL(audioBlob),
          })
        }
      }
      setStems(extracted)
    } catch (err) {
      console.error(err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='container'>
      <h1>Разделение аудио</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".mp3,.wav" onChange={handleFileChange} required />
        <button type="submit" disabled={loading || !file}>
          {loading ? 'Обработка...' : 'Разделить'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>❌ {error}</p>}

      {stems.length > 0 && (
        <div>
          <h2>Стемы:</h2>
          {stems.map((stem) => (
            <div key={stem.name} style={{ margin: '10px 0', border: '1px solid #ccc', padding: 10 }}>
              <strong>{stem.name}</strong>
              <br />
              <audio controls src={stem.url} style={{ width: '100%', maxWidth: 400 }} />
              <br />
              <a href={stem.url} download={`${stem.name}.wav`}>
                ⬇️ Скачать {stem.name}.wav
              </a>
            </div>
          ))}
          {zipUrl && (
            <div style={{ marginTop: 20 }}>
              <a href={zipUrl} download="stems.zip">
                💾 Скачать всё (ZIP)
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App