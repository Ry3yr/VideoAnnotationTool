# Video Annotation Tool

A browser-based tool to annotate your videos **after recording** with precise audio overlays. Generates exact FFmpeg commands to merge audio snippets into your video timeline.

## Features

- **100% client-side HTML/JS** – No backend, no installation, no dependencies
- **Post-recording annotation** – Add audio comments, corrections, or narration over existing tracks
- **FFmpeg command generation** – Outputs ready-to-use merge commands
- **Batch import** – Auto-place audio files by filename timestamp:
  - `hh_mm_ss_name.mp3` (e.g., `01_15_30_correction.mp3`)
  - `mm_ss_name.mp3` (e.g., `05_45_note.mp3`)

- **Qwen3-TTS integration** – [Optional] Generate custom voice snippets via [QwenTTS](https://github.com/QwenLM/Qwen3-TTS) API
- **SRT parser** – Upload subtitle files to auto-generate annotation timestamps
(Subtitles can be extracted from onscreen text via: https://github.com/timminator/VideOCR/releases/download/v1.5.1/VideOCR-GPU-v1.5.1-CUDA-12.9-setup-x64.exe )
  
## Quick Start

### Just open the HTML file

1. **Download** `annotation-tool.html`
2. **Double-click** to open in any modern browser
3. **Start annotating** – no server, no install.
