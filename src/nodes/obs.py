from src.state.state import ProcessState
from src.tools.obs import OBS

def record_video(state: ProcessState) -> ProcessState:
        try:
            recording_path = OBS()
            if recording_path:
                state["recording_path"] = recording_path
                state["status"] = "recording_complete"
            else:
                state["error"] = "Failed to record video"
                state["status"] = "failed"
        except Exception as e:
            state["error"] = str(e)
            state["status"] = "failed"
        return state