# TTS on Colab

A small text-to-speech HTTP server that runs comfortably on Google Colab's free GPU, powered by [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M). Send it a list of narration strings, get back WAV audio and SRT subtitles per scene.

## Run on Colab

1. Open `colab.ipynb` in Google Colab.
2. Run all cells. The third cell starts the FastAPI server on port 5000 and opens a [localtunnel](https://github.com/localtunnel/localtunnel) so you can reach it from outside Colab.
3. The public tunnel URL is printed in the cell output — use that as `BASE_URL` in your client.

## Run locally

```bash
pip install -r requirements.txt
python api.py
```

Server listens on `http://0.0.0.0:5000`.

## API

`POST /generate-audio-and-subtitles`

```json
{
  "scenes": ["First narration.", "Second narration."],
  "voice": "am_liam"
}
```

Response:

```json
{
  "scenes": [
    {"audio": "<base64 WAV>", "srt": "<SRT text>"}
  ]
}
```

Available voices are listed in [Kokoro's VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).

## Client example

See `example.py` for a minimal client that POSTs scenes and writes `.wav` + `.srt` files to disk.
