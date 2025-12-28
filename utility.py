import os
from uuid import uuid4
import edge_tts
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

# ==================================================
# 🎙️ TEXT TO SPEECH (FIXED VOICE)
# ==================================================

DEFAULT_VOICE = "en-US-MichelleNeural"

async def TTS(
    text: str,
    output_dir: str = "tts_outputs",
    rate: str = "+0%",
    pitch: str = "+0Hz"
) -> str:

    if not text.strip():
        raise ValueError("Empty text")

    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid4().hex}.mp3"
    output_path = os.path.join(output_dir, filename)

    communicate = edge_tts.Communicate(
        text=text,
        voice=DEFAULT_VOICE,
        rate=rate,
        pitch=pitch
    )

    await communicate.save(output_path)
    return output_path


# ==================================================
# 🎧 SPEECH TO TEXT
# ==================================================

async def STT(audio_file):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{uuid4().hex}.wav"

    with open(file_path, "wb") as f:
        f.write(await audio_file.read())

    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            temperature=0.0
        )

    return {
        "text": transcription.text,
        "segments": transcription.segments,
        "language": transcription.language
    }
