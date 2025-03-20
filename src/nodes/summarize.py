import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

# Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_text(transcribed_text):
    try:
        # Initialize the ChatGroq model with Mixtral (corrected from qwen)
        chat_model = ChatGroq(
            model_name="mixtral-8x7b-32768",  # Correct model for summarization
            api_key=GROQ_API_KEY
        )
        
        # Clearer prompt structure
        messages = [
            SystemMessage(content="You are an expert technical writer skilled in creating structured and professional summaries."),
            HumanMessage(content=f"""Summarize the following meeting discussion in a structured format. The summary should capture all key points, decisions made, action items, and important takeaways. 

        **Format:**
        1. **Agenda**: [Summarize the purpose of the meeting]
        2. **Key Discussions**: [List major topics discussed]
        3. **Decisions Made**: [Highlight any conclusions or agreements]
        4. **Action Items & Responsibilities**: [Clearly mention next steps and assigned persons]
        5. **Additional Notes**: [Any other relevant details]

        Ensure the summary is concise (within 300 words) and formatted clearly.

        **Meeting Transcript:**  
        {transcribed_text}""")
        ]

        
        response = chat_model.invoke(messages)
        return response.content
    
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage with a transcript file
transcript_file_path = "recordings_dir/original_transcript.txt"

# Read the transcribed text from the file
if os.path.exists(transcript_file_path):
    with open(transcript_file_path, "r", encoding="utf-8") as file:
        transcribed_text = file.read()
    
    summary = summarize_text(transcribed_text)
    
    # Save summary inside recordings_dir
    summary_file_path = "recordings_dir/original_summary.txt"
    with open(summary_file_path, "w", encoding="utf-8") as file:
        file.write(summary)
else:
    print(f"Error: Transcript file not found at {transcript_file_path}")