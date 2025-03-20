from langgraph.graph import StateGraph, END
from typing import Dict, TypedDict, Annotated
from src.state.state import ProcessState, init_process_state
from src.nodes.obs import record_video
from src.nodes.text import process_transcription
from src.nodes.summarize import generate_summary
from src.nodes.error_handler import handle_processing_errors
from src.LLMS.groq_LLM import initialize_llm

def create_workflow_graph(groq_api_key: str):
    """Create a workflow graph for processing videos"""
    # Initialize the graph and LLM
    workflow = StateGraph(ProcessState)
    llm = initialize_llm(groq_api_key)

    # Add nodes to graph
    workflow.add_node("record", record_video)
    workflow.add_node("transcribe", lambda x: process_transcription(x, groq_api_key))
    workflow.add_node("summarize", lambda x: generate_summary(x, groq_api_key))
    workflow.add_node("error_handler", handle_processing_errors)

    # Define edges
    workflow.set_entry_point("record")
    workflow.add_edge("record", "transcribe")
    workflow.add_edge("transcribe", "summarize")
    workflow.add_edge("summarize", END)
    workflow.add_edge("error_handler", END)

    # Conditional edges with centralized error handling
    workflow.add_conditional_edges(
        "record",
        lambda x: "error_handler" if x["status"] == "failed" else "transcribe"
    )
    workflow.add_conditional_edges(
        "transcribe",
        lambda x: "error_handler" if x["status"] == "failed" else "summarize"
    )
    workflow.add_conditional_edges(
        "summarize",
        lambda x: "error_handler" if x["status"] == "failed" else END
    )

    # Compile the graph
    app = workflow.compile()
    return app

def execute_workflow(groq_api_key: str):
    """Execute the complete workflow from recording to summary"""
    try:
        workflow = create_workflow_graph(groq_api_key)
        initial_state = init_process_state()
        final_state = workflow.invoke(initial_state)
        
        if final_state["status"] == "complete":
            return {
                "success": True,
                "summary": final_state["summary"],
                "recording_path": final_state["recording_path"],
                "transcript_path": final_state["transcript_path"]
            }
        else:
            return {
                "success": False,
                "error": final_state.get("error", "Workflow failed")
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }