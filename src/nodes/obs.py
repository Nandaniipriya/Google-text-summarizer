import time
import os
from dotenv import load_dotenv
from datetime import datetime
from obsws_python import ReqClient

def connect_to_obs():
    load_dotenv()
    password = os.getenv('OBS_PASSWORD')
    
    try:
        # Connect to OBS using the newer protocol
        obs = ReqClient(host='localhost', port=4455, password=password)
        # Test connection with a simple request
        version = obs.get_version()
        print(f"Connected to OBS version: {version.obs_version}")
        print(f"WebSocket version: {version.obs_web_socket_version}")
        return obs
    except Exception as e:
        print(f"Could not connect to OBS: {e}")
        return None

def main():
    # Connect to OBS
    obs = connect_to_obs()
    if not obs:
        return
        
    try:
        # Create recordings directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        recordings_dir = os.path.join(project_root, "recordings_dir")
        if not os.path.exists(recordings_dir):
            os.makedirs(recordings_dir)
        
        # Get current recording settings
        current_dir = obs.get_record_directory()
        print(f"Current recording folder: {current_dir.record_directory}")
        
        # Set new recording path
        print(f"Setting recording folder to: {recordings_dir}")
        obs.set_record_directory(recordings_dir)  # Pass path directly without parameter name
        
        # Verify the change
        new_dir = obs.get_record_directory()
        print(f"Updated recording folder: {new_dir.record_directory}")
        
        # Start recording
        print("Starting recording...")
        obs.start_record()
        
        # Record for 10 seconds
        time.sleep(10)
        
        # Stop recording
        print("Stopping recording...")
        obs.stop_record()
        
        # Give OBS a moment to finish writing the file
        time.sleep(2)
        
        # Check recording status
        try:
            status = obs.get_record_status()
            print(f"Recording active: {status.output_active}")
        except:
            print("Could not get recording status")
        
        # Search for recordings
        print("\nSearching for recordings...")
        if os.path.exists(recordings_dir):
            files = os.listdir(recordings_dir)
            if files:
                print(f"Files in {recordings_dir}:")
                for file in files:
                    if file.endswith('.mp4') or file.endswith('.mkv'):
                        print(f" - {file}")
            else:
                print(f"No files found in {recordings_dir}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()