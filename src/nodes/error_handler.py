from src.state.state import ProcessState

def handle_processing_errors(state: ProcessState) -> ProcessState:
    """Centralized error handler for the workflow"""
    error_message = state.get("error", "Unknown error occurred")
    print(f"Error in workflow: {error_message}")
    state["status"] = "error_handled"
    return state