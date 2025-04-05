# -------------------- Load Environment Variables --------------------
from dotenv import load_dotenv
load_dotenv()

# -------------------- Imports --------------------
import os
import platform
import subprocess
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs

# -------------------- Get ElevenLabs API Key --------------------
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# -------------------- gTTS (Google Text-to-Speech) - Basic --------------------
def text_to_speech_with_gtts_old(input_text, output_filepath):
    """
    Convert text to speech using gTTS and save the result to an MP3 file.
    (Old version without autoplay)
    """
    language = "en"
    audio = gTTS(text=input_text, lang=language, slow=False)
    audio.save(output_filepath)

# -------------------- ElevenLabs Text-to-Speech - Basic --------------------
def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs and save the result to an MP3 file.
    (Old version without autoplay)
    """
    print("API KEY exists:", bool(ELEVENLABS_API_KEY))
    print(f"Generating speech for: {input_text}")
    
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    try:
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
        print(f"✅ File saved to {output_filepath}")
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

# -------------------- gTTS with Autoplay --------------------
def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Convert text to speech using gTTS, save it, and automatically play the audio.
    """
    language = "en"
    audio = gTTS(text=input_text, lang=language, slow=False)
    audio.save(output_filepath)

    # Detect operating system and play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])  # You can also use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# -------------------- ElevenLabs with Autoplay --------------------
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs, save it, and automatically play the audio.
    """
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

    # Detect operating system and play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# -------------------- Example Usage --------------------
if __name__ == "__main__":
    input_text = "Hi, this is Farshad testing ElevenLabs text-to-speech with autoplay!"
    
    # Option 1: Test gTTS with autoplay
    # text_to_speech_with_gtts(input_text, output_filepath="gtts_testing_autoplay.mp3")

    # Option 2: Test ElevenLabs with autoplay
    text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")
