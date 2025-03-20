from src.graph.graph import execute_workflow
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
result = execute_workflow(groq_api_key)

if result["success"]:
    print("Workflow completed successfully!")
    print(f"Summary: {result['summary']}")
else:
    print(f"Error: {result['error']}")