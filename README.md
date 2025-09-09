# Video-to-Transcript Generator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

Easily convert videos into clean, searchable transcripts and subtitles. This project provides a robust pipeline to **extract audio, transcribe speech, diarize speakers, translate, summarize, and export** to multiple formats (TXT, JSON, SRT, VTT).

> **Why this project?**  
> Stop wasting time taking manual notes from videos! Automate the process with state-of-the-art **speech-to-text (STT)** engines, built for both personal and enterprise use.

---

## ✨ Features

- **Multiple input sources**: Local files (`.mp4`, `.mkv`, `.mov`), YouTube, Vimeo, or raw audio.  
- **High-quality transcription**: Switch easily between Whisper, Faster-Whisper, Gemini STT, AssemblyAI, and more.  
- **Speaker diarization**: Optional speaker labels for interviews, podcasts, or meetings.  
- **Timestamps & segmentation**: Word- and sentence-level timestamps with smart punctuation.  
- **Summaries & highlights**: Get concise summaries or key points using your preferred LLM.  
- **Subtitle exports**: Generate `.srt` and `.vtt` files for video platforms.  
- **Batch processing**: Handle entire folders of videos at once.  
- **CLI & Python API**: Command-line ease and integration flexibility.  
- **Extensible**: Easily add new STT models or custom workflows.  
- **Cross-platform**: Works on Windows, macOS, and Linux.  

---

## 🏗️ Architecture

```mermaid
flowchart LR
  A[Video/Audio Input] -->|ffmpeg| B[Audio Extraction]
  B --> C[Transcription Backend]
  C --> D{Post-process}
  D -->|Punctuation & Cleanup| E[Clean Transcript]
  D -->|Diarization| F[Speaker Labels]
  D -->|Translation| G[Translated Text]
  E --> H[Summaries and Highlights via LLM]
  F --> H
  G --> H
  H --> I[Exporters: TXT, JSON, SRT, VTT]
