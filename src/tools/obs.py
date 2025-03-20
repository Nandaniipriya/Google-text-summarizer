import time
import os
from dotenv import load_dotenv
from datetime import datetime
from obsws_python import ReqClient

def connect_to_obs():
    load_dotenv()
    password = os.getenv('OBS_PASSWORD')
    
    try:
        obs = ReqClient(host='localhost', port=4455, password=password)
        version = obs.get_version()
        print(f"Connected to OBS version: {version.obs_version}")
        print(f"WebSocket version: {version.obs_web_socket_version}")
        return obs
    except Exception as e:
        print(f"Could not connect to OBS: {e}")
        return None

def OBS():
    obs = connect_to_obs()
    if not obs:
        return None
        
    try:
        # Create recordings directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        recordings_dir = os.path.join(project_root, "recordings_dir")
        if not os.path.exists(recordings_dir):
            os.makedirs(recordings_dir)
        
        # Set and verify recording path
        print(f"Setting recording folder to: {recordings_dir}")
        obs.set_record_directory(recordings_dir)
        
        # Get initial file count
        initial_files = set(os.listdir(recordings_dir))
        
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
        
        # Get new file list and find the new recording
        final_files = set(os.listdir(recordings_dir))
        new_files = final_files - initial_files
        
        if new_files:
            new_recording = list(new_files)[0]
            recording_path = os.path.join(recordings_dir, new_recording)
            print(f"Recording saved to: {recording_path}")
            return recording_path
        else:
            print("No new recording file found")
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None