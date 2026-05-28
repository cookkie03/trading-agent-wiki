#!/usr/bin/env python3
"""Transcribe WhatsApp opus audio files and save as .transcription.md"""

import datetime
import subprocess
import sys
from pathlib import Path

AUDIO_DIR = Path("/Users/luca/Library/Mobile Documents/iCloud~md~obsidian/Documents/trading-agent-wiki/raw/audio/WhatsApp Chat - Salvatore Luca")

def process(audio: Path) -> None:
    tx = audio.parent / (audio.name + ".transcription.md")
    if tx.exists():
        print(f"⏭️  {audio.name} (already transcribed)")
        return

    print(f"🎙️  {audio.name}")

    # Convert opus -> mp3
    tmp_mp3 = audio.parent / (audio.stem + ".tmp.mp3")
    res = subprocess.run(
        ["ffmpeg", "-y", "-i", str(audio), "-vn", "-ar", "16000", "-ac", "1",
         "-c:a", "libmp3lame", "-q:a", "2", str(tmp_mp3)],
        capture_output=True, text=True
    )
    if res.returncode != 0:
        print(f"❌ ffmpeg error: {res.stderr[:200]}", file=sys.stderr)
        return

    # Transcribe
    res2 = subprocess.run(
        ["whisper", str(tmp_mp3), "--model", "medium", "--output_format", "txt",
         "--output_dir", str(audio.parent)],
        capture_output=True, text=True
    )
    tmp_mp3.unlink(missing_ok=True)

    if res2.returncode != 0:
        print(f"❌ whisper error: {res2.stderr[:200]}", file=sys.stderr)
        return

    txt = audio.parent / (tmp_mp3.stem + ".txt")
    if not txt.exists():
        print(f"❌ whisper output missing: {txt}", file=sys.stderr)
        return

    text = txt.read_text(encoding="utf-8")
    txt.unlink()

    content = (
        "---\n"
        f'source_audio: "{audio.name}"\n'
        f"transcribed_at: {datetime.datetime.now().isoformat()}\n"
        "tool: whisper\n"
        "model: medium\n"
        "---\n\n"
        f"# Transcription: {audio.stem}\n\n"
        f"{text}\n"
    )
    tx.write_text(content, encoding="utf-8")
    print(f"   ✅ {tx.name}")

for f in sorted(AUDIO_DIR.glob("*.opus")):
    process(f)

print("Done.")
