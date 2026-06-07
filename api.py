import base64
import threading
import uvicorn
from fastapi import FastAPI, Body
from tts import make_audio_and_subtitles, VOICE


app = FastAPI()


@app.post("/generate-audio-and-subtitles")
async def generate(scenes: list[str] = Body(...), voice: str = Body(VOICE)):
    results = make_audio_and_subtitles(scenes, voice)
    return {
        "scenes": [
            {"audio": base64.b64encode(wav).decode("ascii"), "srt": srt}
            for wav, srt in results
        ]
    }


def start_server():
    def run():
        uvicorn.run(app, host="0.0.0.0", port=5000)

    threading.Thread(target=run).start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
