from agents import function_tool
from utils.pdf_extractor import extract_text_from_pdf
from utils.quiz_generator import generate_quiz
import json

@function_tool
def summarize_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF and returns a placeholder summary (first 1000 characters).
    In a real scenario, this would involve an LLM call for summarization.
    """
    print(f"--- summarize_pdf tool called for: {file_path} ---")
    text = extract_text_from_pdf(file_path)
    if not text:
        return "Could not extract text from PDF or PDF is empty."
    return text[:1000] # Placeholder summarization

@function_tool
def create_quiz(file_path: str, style: str = "MCQ") -> str: # Changed return type hint to str
    """
    Extracts text from a PDF and generates a quiz (MCQ or mixed style).
    """
    print(f"--- create_quiz tool called for: {file_path} with style: {style} ---")
    text = extract_text_from_pdf(file_path)
    if not text:
        return json.dumps([{"error": "Could not extract text from PDF or PDF is empty."}]) # Return JSON string
    quiz = generate_quiz(text, style=style)
    return json.dumps(quiz) # Return JSON string