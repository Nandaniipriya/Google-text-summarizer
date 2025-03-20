from src.state.state import ProcessState
from src.tools.text import transcribe_audio

def process_transcription(state: ProcessState, groq_api_key: str) -> ProcessState:
    try:
        if state["recording_path"]:
            transcript_path = transcribe_audio(state["recording_path"], groq_api_key)
            if transcript_path:
                state["transcript_path"] = transcript_path
                state["status"] = "transcription_complete"
            else:
                state["error"] = "Failed to transcribe audio"
                state["status"] = "failed"
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
    return state