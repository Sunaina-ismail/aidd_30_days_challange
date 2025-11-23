import os
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
from tools import summarize_pdf, create_quiz
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Configure AsyncOpenAI for Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("Warning: GEMINI_API_KEY environment variable not set. Using dummy key. API calls will likely fail.")
    gemini_api_key = "dummy_key_for_testing"

# Gemini API Base URL and Model Name for better code readability and clarity
GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODEL_NAME = "gemini-2.0-flash"

openai_client = AsyncOpenAI(
    base_url=GEMINI_API_BASE_URL,
    api_key=gemini_api_key,
)

# Initialize OpenAIChatCompletionsModel for Gemini
gemini_model = OpenAIChatCompletionsModel(
    model=GEMINI_MODEL_NAME,
    openai_client=openai_client,
)

# Agent Configuration
# Instructions guide the agent's behavior and tool usage.
agent = Agent(
    name="PDF Assistant",
    instructions=(
        "You are a helpful PDF assistant. Your primary goal is to summarize PDF documents "
        "and generate quizzes based on their content. Always use the provided tools "
        "(summarize_pdf and create_quiz) when appropriate. "
        "When asked to generate a quiz, ensure the output is a pure JSON list of dictionaries, "
        "suitable for direct parsing, and avoid conversational text around the JSON."
    ),
    tools=[summarize_pdf, create_quiz],
    model=gemini_model,
)