from src.state.state import ProcessState
from src.tools.summarize import summarize_text

def generate_summary(state: ProcessState, groq_api_key: str) -> ProcessState:
    try:
        if state["transcript_path"]:
            with open(state["transcript_path"], "r", encoding="utf-8") as f:
                transcribed_text = f.read()
            summary = summarize_text(transcribed_text, groq_api_key)
            if summary:
                state["summary"] = summary
                state["status"] = "complete"
            else:
                state["error"] = "Failed to generate summary"
                state["status"] = "failed"
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
    return state