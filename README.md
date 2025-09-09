# Video‑to‑Transcript Generator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

Turn any video into clean, searchable transcripts and subtitles — fast. This repository provides a production‑ready pipeline to extract audio, transcribe speech, optionally diarize speakers, translate, summarize, and export to multiple formats (TXT/JSON/SRT/VTT).

> **Why this project?**  
> Tired of manually taking notes from videos? This tool automates the entire process with modern speech‑to‑text (STT) engines and a clean developer experience, suitable for personal workflows or internal knowledge assistants.

---

## ✨ Features

- **Multiple inputs**: Local files (`.mp4`, `.mkv`, `.mov`), URLs (YouTube, Vimeo), or raw audio.
- **Robust transcription**: Plug‑and‑play backends (OpenAI Whisper, Faster‑Whisper, Google/Gemini STT, AssemblyAI, etc.).
- **Speaker diarization (optional)**: Label speakers (`Speaker 1`, `Speaker 2`, …) for interviews/podcasts.
- **Chunking & timestamps**: Word‑ and sentence‑level timestamps with smart punctuation.
- **Summaries & highlights**: Auto‑summaries/key points via your LLM of choice (optional).
- **Subtitle exports**: Generate `.srt`/`.vtt` with proper timings; perfect for uploads.
- **Batch mode**: Process whole folders in one go.
- **CLI + Python API**: Use from the terminal or integrate in your own code.
- **Extensible**: Clear interfaces for adding new STT providers and post‑processors.
- **Cross‑platform**: Works on Windows, macOS, Linux; optional Docker image.

---

## 🏗️ Architecture

```mermaid
flowchart LR
  A[Video/Audio Input] -->|ffmpeg| B[Audio Extraction]
  B --> C[Transcription Backend]
  C --> D{Post‑process}
  D -->|Punctuation & Cleanup| E[Clean Transcript]
  D -->|Diarization| F[Speaker Labels]
  D -->|Translation| G[Translated Text]
  E --> H[Summaries/Highlights (LLM)]
  F --> H
  G --> H
  H --> I[Exporters: TXT / JSON / SRT / VTT]
```

---

## 🔧 Tech Stack (default)

- **Language**: Python 3.9+  
- **Core**: `ffmpeg`, `faster‑whisper` (or `openai-whisper`)  
- **Optional**: `yt-dlp` for URL downloads, `pydub` for audio ops, `pyannote.audio` for diarization  
- **LLM/Summary (optional)**: Google Gemini / OpenAI / others via simple adapter

> You can swap components via config flags without changing code.

---

## 📦 Installation

### 1) System prerequisites
- Python **3.9+**
- `ffmpeg` available on PATH  
  - Windows (scoop/choco), macOS (`brew install ffmpeg`), Linux (`apt-get install ffmpeg`).

### 2) Clone
```bash
git clone https://github.com/nitin-pandita/Video-to-Transcript-Generator.git
cd Video-to-Transcript-Generator
```

### 3) Create & activate venv
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 4) Install dependencies
```bash
pip install -r requirements.txt
```
> If you don't yet have a `requirements.txt`, see the suggested one below.

---

## 🚀 Quick Start (CLI)

```bash
# Local video -> transcript + SRT
python -m vttg.cli transcribe "samples/talk.mp4" --model small --srt --vtt --out out/

# YouTube URL -> transcript only
python -m vttg.cli transcribe "https://www.youtube.com/watch?v=<id>" --out out/

# Diarization + summary (requires optional deps + LLM key)
python -m vttg.cli transcribe samples/podcast.mp3 --diarize --summarize --llm gemini --out out/
```

**Outputs (in `out/`):**
- `talk.transcript.txt`
- `talk.transcript.json` (timestamps & metadata)
- `talk.subtitles.srt`
- `talk.subtitles.vtt`
- `talk.summary.md` *(if `--summarize`)*

---

## ⚙️ Configuration

Environment variables (use `.env` or your secrets manager):

| Variable | Purpose | Example |
|---|---|---|
| `STT_BACKEND` | `faster-whisper`, `openai-whisper`, `gemini`, `assemblyai`, … | `faster-whisper` |
| `WHISPER_MODEL` | Whisper model size | `small`, `medium`, `large-v3` |
| `GEMINI_API_KEY` | Required if using Gemini for STT/summary | `AIza...` |
| `OPENAI_API_KEY` | If using OpenAI for summary | `sk-...` |
| `YT_DLP_BIN` | Custom path if not on PATH | `/usr/local/bin/yt-dlp` |

CLI flags override env values. Run `python -m vttg.cli --help` for all options.

---

## 🧰 Python Usage (API)

```python
from vttg import Transcriber, ExportFormat

t = Transcriber(
    backend="faster-whisper",
    model_size="small",
    diarize=False,
    summarize=False,
)

result = t.transcribe("samples/talk.mp4")
# Access segments, timestamps, speaker labels
for seg in result.segments:
    print(f"[{seg.start:.2f}–{seg.end:.2f}] {seg.speaker}: {seg.text}")

# Exports
t.export(result, path="out/talk", formats=[
    ExportFormat.TXT, ExportFormat.JSON, ExportFormat.SRT, ExportFormat.VTT
])
```

---

## 📝 Recommended `requirements.txt`

> Use or adapt as needed.

```
faster-whisper>=1.0.0
ffmpeg-python>=0.2.0
pydub>=0.25.1
yt-dlp>=2024.03.10
tqdm>=4.66.0
python-dotenv>=1.0.1
click>=8.1.7
rich>=13.7.0
# Optional
openai-whisper>=20231117
pyannote.audio>=3.1.1
google-generativeai>=0.7.0
```
> Note: `pyannote.audio` has PyTorch/CUDA requirements. Install per their docs if you enable diarization.

---

## 🧪 Examples

```bash
# 1) Fast local transcription (CPU)
python -m vttg.cli transcribe samples/talk.mp4 --model small

# 2) Highest accuracy (GPU recommended)
python -m vttg.cli transcribe samples/talk.mp4 --model large-v3 --beam-size 5

# 3) Translate to English
python -m vttg.cli transcribe samples/hindi_news.mp4 --translate en --srt --out out/

# 4) Batch a folder
python -m vttg.cli batch "dataset/*.mp4" --out out/batch
```

---

## 🧩 Troubleshooting

- **`ffmpeg not found`**: Ensure `ffmpeg` is installed and on PATH. Run `ffmpeg -version` to confirm.
- **CUDA/GPU issues**: Install PyTorch with the correct CUDA version before `faster-whisper`.
- **Rate limits / API errors**: If using hosted STT/LLM, check your API keys and quotas.
- **YouTube downloads failing**: Keep `yt-dlp` updated: `python -m pip install -U yt-dlp`.

---

## 🗺️ Roadmap

- [ ] Web UI (Streamlit) for drag‑and‑drop uploads
- [ ] Word‑level timestamps in JSON
- [ ] Inline speaker change markers in SRT
- [ ] Post‑processing rules for filler removal
- [ ] Vector search over transcripts (RAG integration)

Have ideas? Open an issue or start a discussion!

---

## 🤝 Contributing

Contributions are welcome! Please:  
1. Fork the repo & create a feature branch.  
2. Follow code style and add tests when possible.  
3. Open a PR with a clear description/screenshots.

See `CONTRIBUTING.md` (create one if missing) for details.

---

## 📄 License

This project is licensed under the **MIT License** — see `LICENSE` for details.

---

## 🙌 Acknowledgements

- OpenAI Whisper / Faster‑Whisper
- `ffmpeg`, `yt-dlp`, and the open‑source audio community
- Google Gemini / OpenAI (for optional summaries)
- Everyone who stars ⭐ and contributes!

---

