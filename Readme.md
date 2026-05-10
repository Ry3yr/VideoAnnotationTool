# 🎥 Video Annotation Tool

Annotate your videos **after** recording with precise audio overlays. Generate exact FFmpeg commands to merge audio snippets into your video timeline.

## ✨ Features

- **Post-recording annotation** – Add audio comments, corrections, or narration over existing tracks
- **FFmpeg command generation** – Outputs ready-to-use merge commands
- **Batch import** – Auto-place audio files by filename timestamp:
  - `hh_mm_ss_name.mp3` (e.g., `01_15_30_correction.mp3`)
  - `mm_ss_name.mp3` (e.g., `05_45_note.mp3`)
- **Qwen3-TTS integration** – Generate custom voice snippets using [QwenTTS](https://github.com/QwenLM/Qwen3-TTS)
- **SRT parser** – Included for subtitle/sync point handling

## 🚀 Quick Start

### Prerequisites
- [FFmpeg](https://ffmpeg.org/) installed and in PATH
- Python 3.8+ (for TTS tools)

### Installation

```bash
git clone https://github.com/yourusername/video-annotation-tool.git
cd video-annotation-tool
pip install -r requirements.txt  # if using TTS features