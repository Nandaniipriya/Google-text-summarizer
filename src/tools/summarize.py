import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

def summarize_text(transcribed_text,GROQ_API_KEY):
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