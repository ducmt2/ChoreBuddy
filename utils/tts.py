import os
import logging

from gtts import gTTS
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
#   Load environment variables
# ---------------------------------------------------------------------------

load_dotenv()

_player = os.environ.get("TTS_PLAYER")
logging.info("TTS player: %s", _player)


# ---------------------------------------------------------------------------
#   Text to speech
# ---------------------------------------------------------------------------


def play_text(script: str) -> None:
    logging.info("TTS >>> %s", script)
    if len(script) == 0:
        return

    tts = gTTS(text=script, lang="en")
    tts.save("out.mp3")

    if _player == "VLC":
        os.system("vlc --play-and-exit out.mp3")
    else:
        os.system("ffplay -nodisp -autoexit -loglevel error out.mp3")
