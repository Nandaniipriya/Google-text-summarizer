import os
from dotenv import load_dotenv
from pydub import AudioSegment
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load API Key from environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Function to transcribe audio using Groq API through LangChain
def transcribe_audio(audio_path):
    try:
        # Convert audio to MP3 format (if not already)
        converted_path = os.path.splitext(audio_path)[0] + "_converted.mp3"
        audio = AudioSegment.from_file(audio_path)
        audio.export(converted_path, format="mp3")

        print(f"Processing audio file: {converted_path}")

        # Initialize the ChatGroq client
        chat_client = ChatGroq(
            model="whisper-large-v3",
            groq_api_key=GROQ_API_KEY
        )

        # For audio transcription with Whisper, we need to use a different approach
        # as ChatGroq doesn't directly support audio files in messages
        
        # Import the necessary Groq client directly
        from groq import Groq
        
        client = Groq(api_key=GROQ_API_KEY)
        
        with open(converted_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                language="en",
                response_format="text"
            )
        
        # Extract the transcription text
        transcription = response
        print("Transcription completed successfully.")
        return transcription

    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

# Example usage
audio_file_path = "recordings_dir\original.mp4"  # Update this path to the correct audio file location
transcription = transcribe_audio(audio_file_path)

if transcription:
    print("\nTranscribed Text:\n", transcription)