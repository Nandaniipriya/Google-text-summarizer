from typing import Dict, TypedDict, List
from typing_extensions import Annotated
from langchain_core.messages import BaseMessage

class ProcessState(TypedDict):
    recording_path: str
    transcript_path: str
    summary: str
    error: str
    status: str

def init_process_state() -> ProcessState:
    return ProcessState(
        recording_path="",
        transcript_path="",
        summary="",
        error="",
        status="initialized"
    )