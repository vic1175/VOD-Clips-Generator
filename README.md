# OBS VOD Clip Extractor

A lightweight, automated desktop tool built in Python using `Tkinter` and `yt-dlp` to parse local OBS Stream Marker CSV files and instantly extract highlighted clips from finished YouTube VOD streams.

## Features
* **Auto-Rewind Math:** Automatically extracts the 60 seconds of video right *before* you pressed your hotkey.
* **Custom Naming:** Reads custom names straight out of Column B from your modified marker spreadsheet.
* **Format-Immune:** Handles single-digit hour shifts smoothly (`1:15:00` vs `01:15:00`).

## Prerequisites
1. **Python 3.x** installed.
2. **FFmpeg** installed locally (placed at `C:\ffmpeg\bin\ffmpeg.exe`).

## Installation & Setup
1. Clone or download this repository.
2. Install dependencies via command prompt:
   ```bash
   pip install yt-dlp pyinstaller