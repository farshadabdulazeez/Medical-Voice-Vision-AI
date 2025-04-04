# import logging
# import os
# from io import BytesIO

# # Step 1: Setup Audio Recording
# import speech_recognition as sr
# from pydub import AudioSegment

# # Step 2: Load Environment Variables
# from dotenv import load_dotenv
# load_dotenv() 

# # Step 3: Setup Groq Whisper API for Transcription
# from groq import Groq

# # ---------------------------- Configuration ---------------------------- #

# # Configure logging for better traceability
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Path to save the recorded patient voice input
# AUDIO_FILE_PATH = "patient_query_test.mp3"

# # Whisper model from Groq
# STT_MODEL = "whisper-large-v3"

# # API Key (Ensure it's set in your .env or system environment variables)
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # ------------------------ Audio Recording Function --------------------- #

# def record_audio(file_path, timeout=20, phrase_time_limit=None):
#     """
#     Records audio from the default microphone and saves it as an MP3.

#     Args:
#         file_path (str): File path where the MP3 will be saved.
#         timeout (int): Max time to wait for the user to start speaking.
#         phrase_time_limit (int): Max length of recorded phrase.
#     """
#     recognizer = sr.Recognizer()

#     try:
#         with sr.Microphone() as source:
#             logging.info("Adjusting for ambient noise...")
#             recognizer.adjust_for_ambient_noise(source, duration=1)

#             logging.info("Listening... Please start speaking.")
#             audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#             logging.info("Audio recording complete.")

#             # Convert to MP3 using pydub
#             wav_data = audio_data.get_wav_data()
#             audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
#             audio_segment.export(file_path, format="mp3", bitrate="128k")

#             logging.info(f"Audio saved successfully to: {file_path}")

#     except Exception as e:
#         logging.error(f"Recording failed: {e}")

# # --------------------- Transcription Function -------------------------- #

# def transcribe_with_groq(model, audio_filepath, api_key):
#     """
#     Transcribes an audio file using Groq's Whisper model.

#     Args:
#         model (str): Whisper model version.
#         audio_filepath (str): Path to the audio file to transcribe.
#         api_key (str): Your Groq API key.

#     Returns:
#         str: Transcribed text.
#     """
#     try:
#         client = Groq(api_key=api_key)
#         with open(audio_filepath, "rb") as audio_file:
#             logging.info("Sending audio to Groq for transcription...")
#             transcription = client.audio.transcriptions.create(
#                 model=model,
#                 file=audio_file,
#                 language="en"
#             )
#         logging.info("Transcription complete.")
#         return transcription.text

#     except Exception as e:
#         logging.error(f"Transcription failed: {e}")
#         return ""

# # -------------------------- Main Execution ----------------------------- #

# if __name__ == "__main__":
#     # Step 1: Record the patient's voice query
#     record_audio(AUDIO_FILE_PATH)

#     # Step 2: Transcribe the recorded voice query
#     if os.path.exists(AUDIO_FILE_PATH):
#         result = transcribe_with_groq(STT_MODEL, AUDIO_FILE_PATH, GROQ_API_KEY)
#         print("\n📝 Transcription Result:\n", result)
#     else:
#         logging.error("Audio file not found, skipping transcription.")
import logging
import os
from io import BytesIO

# Step 1: Audio Recording
import speech_recognition as sr
from pydub import AudioSegment

# Step 2: Load Environment Variables
from dotenv import load_dotenv
load_dotenv()

# Step 3: Setup Groq Whisper API
from groq import Groq

# ---------------------------- Configuration ---------------------------- #

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AUDIO_FILE_PATH = "patient_query_test.mp3"
STT_MODEL = "whisper-large-v3"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Debugging API Key load
if GROQ_API_KEY:
    logging.info("✅ GROQ_API_KEY loaded successfully.")
else:
    logging.error("❌ GROQ_API_KEY is missing! Make sure it's set in your .env file or environment variables.")

# ------------------------ Audio Recording Function --------------------- #

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as MP3.

    Args:
        file_path (str): File path to save the audio.
        timeout (int): Max time to wait for the speaker to start.
        phrase_time_limit (int): Max length of the audio phrase.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            logging.info("🎙️ Listening... Please speak now.")
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("✅ Audio recording complete.")

            # Convert to MP3 using pydub
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"📁 Audio saved to: {file_path}")

    except Exception as e:
        logging.error(f"❌ Recording failed: {e}")

# --------------------- Transcription Function -------------------------- #

def transcribe_with_groq(model, audio_filepath, api_key):
    """
    Transcribes the audio file using Groq's Whisper API.

    Args:
        model (str): Whisper model name.
        audio_filepath (str): Path to the MP3 file.
        api_key (str): GROQ API Key.

    Returns:
        str: Transcribed text or empty string.
    """
    try:
        logging.info(f"🔍 Preparing to transcribe with model: {model}")
        client = Groq(api_key=api_key)

        with open(audio_filepath, "rb") as audio_file:
            logging.info("📤 Sending audio to Groq for transcription...")
            transcription = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language="en"
            )

        logging.info("✅ Transcription complete.")
        logging.debug(f"🧾 Full transcription response: {transcription}")
        return transcription.text

    except Exception as e:
        logging.error(f"❌ Transcription failed: {e}")
        return ""

# -------------------------- Main Execution ----------------------------- #

if __name__ == "__main__":
    if not GROQ_API_KEY:
        logging.error("❌ Cannot continue without GROQ_API_KEY.")
    else:
        # Step 1: Record patient's voice
        record_audio(AUDIO_FILE_PATH)

        # Step 2: Transcribe the voice
        if os.path.exists(AUDIO_FILE_PATH):
            result = transcribe_with_groq(STT_MODEL, AUDIO_FILE_PATH, GROQ_API_KEY)
            if result:
                print("\n📝 Transcription Result:\n", result)
            else:
                logging.warning("⚠️ No transcription result received.")
        else:
            logging.error("❌ Audio file not found. Skipping transcription.")
