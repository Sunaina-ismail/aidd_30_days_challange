def generate_quiz(text: str, style: str = "MCQ") -> list:
    """
    Generates a placeholder quiz based on the extracted text.
    In a real application, this would involve an LLM call.
    """
    if style == "MCQ":
        return [
            {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome"], "answer": "Paris"},
            {"question": "What is 2+2?", "options": ["3", "4", "5"], "answer": "4"}
        ]
    else:
        return [
            {"question": "Summarize the main topic of the document."},
            {"question": "What is one key takeaway from the text?"}
        ]