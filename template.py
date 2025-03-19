import os
import sys
from pathlib import Path

def create_directory_structure():
    # Define the base project directory
    base_dir = Path(__file__).parent

    # Define the directory structure
    directories = [
        "src",
        "src/LLMS",
        "src/graph",
        "src/nodes",
        "src/state",
        "src/tools",
        "src/UI",
        "src/UI/streamlitUI",
        "src/vectorstore",
        ".github/workflows"
    ]

    # Create directories and __init__.py files
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py in each directory
        init_file = full_path / "__init__.py"
        init_file.touch()

    # Create root level files
    root_files = {
        "app.py": "",
        "requirements.txt": """langchain
langgraph
langchain_community
langchain_core
langchain_groq
langchain_openai
faiss-cpu
streamlit"""
    }

    for filename, content in root_files.items():
        file_path = base_dir / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    # Create .gitkeep in workflows directory
    workflows_gitkeep = base_dir / ".github" / "workflows" / ".gitkeep"
    workflows_gitkeep.touch()

def main():
    try:
        create_directory_structure()
        print("Project structure created successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()