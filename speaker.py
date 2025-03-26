from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from playsound import playsound
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
speech_file_path = Path(__file__).parent / "speech.mp3"

# Create speech
response = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="ballad",
    input="Today is a wonderful day to build something people love!",
    instructions="Speak with an indian accent.",
    speed=1.0,
)
# Write the binary content to file
with open(speech_file_path, "wb") as file:
    file.write(response.content)

# Play the generated audio file
playsound(str(speech_file_path))
