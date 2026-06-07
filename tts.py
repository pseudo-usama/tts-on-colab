# Available voices: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md#american-english
import io
import itertools
import soundfile as sf
from kokoro import KPipeline

VOICE = "am_liam"
SAMPLE_RATE = 24_000    # Hz


def _ts(sec: float) -> str:
    # 00:00:01,234 (SRT format)
    ms = int(round(sec * 1_000))
    hh, ms = divmod(ms, 3_600_000)
    mm, ms = divmod(ms,   60_000)
    ss, ms = divmod(ms,    1_000)

    return f"{hh:02}:{mm:02}:{ss:02},{ms:03}"


def _generate(text: str, voice: str) -> tuple[bytes, str]:
    pipeline = KPipeline(lang_code="a")  # American English

    captions = []       # [(idx, start, end, word), ...]
    offset_sec = 0.0    # how far into the whole audio we are
    idx = itertools.count(1)
    audio = None

    for i, result in enumerate(pipeline(text, voice=voice)):
        if i > 0:
            raise RuntimeError("Kokoro returned multiple audio chunks; expected one.")

        audio = result.audio.cpu().numpy()

        if result.tokens:               # may be None on quiet chunks
            for tok in result.tokens:
                if tok.phonemes:        # skip whitespace
                    captions.append(
                        (next(idx),
                        offset_sec + tok.start_ts,
                        offset_sec + tok.end_ts,
                        tok.text)
                    )

        offset_sec += len(audio) / SAMPLE_RATE

    wav_buf = io.BytesIO()
    sf.write(wav_buf, audio, SAMPLE_RATE, format="WAV")

    srt = "".join(
        f"{n}\n{_ts(start)} --> {_ts(end)}\n{word}\n\n"
        for n, start, end, word in captions
    )

    return wav_buf.getvalue(), srt


def make_audio_and_subtitles(narrations: list[str], voice: str = VOICE) -> list[tuple[bytes, str]]:
    return [_generate(text, voice) for text in narrations]
