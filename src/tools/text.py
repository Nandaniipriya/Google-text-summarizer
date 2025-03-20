import os
from pydub import AudioSegment
from groq import Groq

def transcribe_audio(audio_path,GROQ_API_KEY):
    try:
        # Create transcripts directory if it doesn't exist
        base_dir = os.path.dirname(audio_path)
        transcript_dir = os.path.join(base_dir, "transcripts")
        os.makedirs(transcript_dir, exist_ok=True)

        # Convert audio to MP3 format
        converted_path = os.path.splitext(audio_path)[0] + "_converted.mp3"
        audio = AudioSegment.from_file(audio_path)
        audio.export(converted_path, format="mp3")

        print(f"Processing audio file: {converted_path}")

        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        with open(converted_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                language="en",
                response_format="text"
            )
        
        # Save transcription to a file inside recordings_dir
        transcript_filename = f"{os.path.splitext(os.path.basename(audio_path))[0]}_transcript.txt"
        transcript_path = os.path.join(base_dir, transcript_filename)

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(response)

        return transcript_path  # Return path instead of printing

    except Exception as e:
        print(f"Error processing audio: {e}")
        return None