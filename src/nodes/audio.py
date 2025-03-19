import os
import subprocess

def extract_audio(recordings_dir):
    try:
        # Find the most recent recording (assuming OBS saves in order)
        files = sorted(
            [f for f in os.listdir(recordings_dir) if f.endswith(('.mp4', '.mkv'))],
            key=lambda x: os.path.getmtime(os.path.join(recordings_dir, x)),
            reverse=True
        )

        if not files:
            print("No recorded video files found.")
            return

        latest_video = files[0]
        video_path = os.path.join(recordings_dir, latest_video)
        audio_path = os.path.splitext(video_path)[0] + ".mp3"  # Convert to MP3 format

        print(f"Extracting audio from: {video_path}")
        
        # FFmpeg command to extract audio
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", video_path,  # Input video file
            "-vn",  # Disable video recording
            "-acodec", "mp3",  # Set audio codec to MP3
            "-y",  # Overwrite if exists
            audio_path  # Output audio file
        ]

        # Run the command
        subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Audio extracted successfully: {audio_path}")

    except Exception as e:
        print(f"Error extracting audio: {e}")

# Example usage
recordings_dir = "E:/Google_text_summarizer/recordings_dir"  # Change this to your actual recording folder
extract_audio(recordings_dir)
