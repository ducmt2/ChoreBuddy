from gtts import gTTS
import os

# The text that needs to be converted to audio
s = "Good morning"
file = "out.mp3"

# Set the language for the engine
language = "en"

# The audio file can be set to have either slow or high speed
# tts = gTTS(text=s, lang=language, slow=False)
tts = gTTS(text=s, lang=language)


# Create mp3 file and play
tts.save(file)
os.system("afplay " + file)
