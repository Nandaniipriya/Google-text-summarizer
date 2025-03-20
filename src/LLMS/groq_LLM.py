import os
import streamlit as st
from langchain_groq import ChatGroq

def initialize_llm(api_key: str, model_name: str = "mixtral-8x7b-32768"):
    """Initialize the Groq LLM with the given API key"""
    try:
        llm = ChatGroq(
            api_key=api_key,
            model_name=model_name
        )
        return llm
    except Exception as e:
        raise ValueError(f"Failed to initialize LLM: {e}")