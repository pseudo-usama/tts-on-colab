"""Example client for the colab_tts server.

Run the server first (`python api.py` locally, or via colab.ipynb on Colab),
then point BASE_URL at it and run this file.

# Available voices: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md#american-english
"""
import base64
import requests
from pathlib import Path


BASE_URL = "https://myttsserver.loca.lt"


def generate(
        scenes: list[str],
        out_dir: str | Path,
        voice: str = "am_liam"
    ):
    """POST a list of narrations and save WAV + SRT for each scene to out_dir."""
    res = requests.post(
        f"{BASE_URL}/generate-audio-and-subtitles",
        json={"scenes": scenes, "voice": voice},
    ).json()

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i, scene in enumerate(res["scenes"], 1):
        (out / f"{i}.wav").write_bytes(base64.b64decode(scene["audio"]))
        (out / f"{i}.srt").write_text(scene["srt"], encoding="utf-8")


if __name__ == "__main__":
    generate(["Hello world.", "This is a second scene."], out_dir="./output")
