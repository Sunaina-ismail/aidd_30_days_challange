# Role: Senior Python AI Engineer

**Objective:** Build a "PDF Summarizer & Quiz Generator Agent" using OpenAgents SDK and Gemini via Gemini CLI. The goal is to  
      develop a web-based agent that allows students to upload a PDF, receive a clean, meaningful summary, and generate quizzes (MCQs
      from the original PDF content).
## 1. Project Overview

**Core Components:**

*   **UI:** Streamlit (modern, responsive)
*   **Model:** Google Gemini `gemini-2.0-flash` via `openai-agents` SDK.
*   **PDF Handling:** `PyPDF2` for text extraction.
*   **Agent Execution:** `openai-agents` SDK.
## 2. Critical Technical Constraints
**Strict configuration rules for development:**

### Zero-Bloat Protocol (CRITICAL)
*   Do not write unnecessary code or features. Focus strictly on: PDF upload → Summarization → Quiz generation.
*   All provided code snippets are the *exact* required implementation; do not add bells, whistles, advanced error handling    
      (unless specified), or unnecessary comments.

### SDK Configuration
*   Use the **`openai-agents` SDK** (not the standard `openai` library).
*   **Model Name:** `gemini-2.0-flash`.
*   **Gemini API Base URL:** `https://generativelanguage.googleapis.com/v1beta/openai/`.
*   Load API Key from `.env` using `GEMINI_API_KEY`.
*   Use `OpenAIChatCompletionsModel` for Gemini integration.

### Tool Integration
*   Tools must be defined using the `@function_tool` decorator.
*   Summarization and quiz generation functions must be registered as agent tools.

### Dependency Management
*   Use `uv` for package management.
 ## 3. Architecture & File Structure
The project will have the following structure in the root directory:
  .
  ├── .env                  # Stores GEMINI_API_KEY
  ├── requirements.txt      # Lists Python dependencies
  ├── tools.py              # PDF summarization & quiz generator functions (as agent tools)
  ├── agent.py              # Agent configuration & tool binding
  ├── app.py                # Streamlit UI & event handlers
  ├── uploaded_pdfs/        # Directory to store user-uploaded PDFs
  └── utils/                # Directory for utility functions
      ├── __init__.py       # Makes 'utils' a Python package
      ├── pdf_extractor.py  # Function to extract text from PDF
      └── quiz_generator.py # Function to generate quiz (placeholder)

## 4. Implementation Steps
**Follow this exact logical flow. Do not skip steps.**

### Step 1: Initialize Project Structure
 First, create the necessary directories and files.
1.  **Create directories:**
      mkdir uploaded_pdfs
      mkdir utils
2.  **Create `utils/__init__.py`:**
      touch utils/__init__.py
*Content for `utils/__init__.py` (leave empty):*
  This file makes 'utils' a Python package.
3.  **Create `.env` file:**
      touch .env
*Content for `.env`:*
      `GEMINI_API_KEY=your_gemini_api_key_here`

### Step 2: Implement Utility Functions
Create the Python files for PDF extraction and quiz generation within the `utils/` directory.
1.  **Create `utils/pdf_extractor.py`:**
      touch utils/pdf_extractor.py

*Content for `utils/pdf_extractor.py`:*

```python
      from PyPDF2 import PdfReader

      def extract_text_from_pdf(file_path: str) -> str:
          """
          Extracts text from a given PDF file.
          """
          text = ""
          try:
              reader = PdfReader(file_path)
              for page in reader.pages:
                  text += page.extract_text() or ""
          except Exception as e:
              print(f"Error extracting text from PDF: {e}")
              return ""
          return text
          ```

2.  **Create `utils/quiz_generator.py`:**
      touch utils/quiz_generator.py
*Content for `utils/quiz_generator.py`:*

```python
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
```

### Step 3: Define Agent Tools (`tools.py`)
Create `tools.py` in the root directory to define the functions that the agent will be able to call.

 1.  **Create `tools.py`:**
      touch tools.py
*Content for `tools.py`:*
```python
      from agents import function_tool
      from utils.pdf_extractor import extract_text_from_pdf
      from utils.quiz_generator import generate_quiz

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
      def create_quiz(file_path: str, style: str = "MCQ") -> list:
          """
          Extracts text from a PDF and generates a quiz (MCQ or mixed style).
          """
          print(f"--- create_quiz tool called for: {file_path} with style: {style} ---")
          text = extract_text_from_pdf(file_path)
          if not text:
              return [{"error": "Could not extract text from PDF or PDF is empty."}]
          quiz = generate_quiz(text, style=style)
          return quiz

   1
   2 ### Step 4: Configure the Agent (`agent.py`)
   3
   4 Create `agent.py` in the root directory to set up the Gemini model and configure the agent with its tools.
   5
   6 1.  **Create `agent.py`:**
      touch agent.py
   1     *Content for `agent.py`:*
      import os
      from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
      from tools import summarize_pdf, create_quiz
      from dotenv import load_dotenv

      load_dotenv() # Load environment variables from .env file

  Configure AsyncOpenAI for Gemini
      gemini_api_key = os.getenv("GEMINI_API_KEY")
      if not gemini_api_key:
          print("Warning: GEMINI_API_KEY environment variable not set. Using dummy key. API calls will likely fail.")
          gemini_api_key = "dummy_key_for_testing"

  Gemini API Base URL and Model Name for better code readability and clarity
      GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
      GEMINI_MODEL_NAME = "gemini-2.0-flash"

      openai_client = AsyncOpenAI(
          base_url=GEMINI_API_BASE_URL,
          api_key=gemini_api_key,
      )

  Initialize OpenAIChatCompletionsModel for Gemini
      gemini_model = OpenAIChatCompletionsModel(
          model=GEMINI_MODEL_NAME,
          openai_client=openai_client,
      )

  Agent Configuration
  Instructions guide the agent's behavior and tool usage.
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
      )```

### Step 5: Build Streamlit UI (`app.py`)

Create `app.py` in the root directory for the Streamlit web interface. This includes the UI for PDF upload, displaying summaries
     and generating/displaying quizzes.

1.  **Create `app.py`:**
      touch app.py
*Content for `app.py`:*
```python
      import streamlit as st
      import os
      import json
      import re
      import ast
      from agent import agent
      from agents import Runner

  Helper function to extract JSON from a Markdown code block
      def extract_json_from_markdown(text: str) -> str:
          """
          Extracts a JSON string from a Markdown code block.
          Assumes the JSON is within a 'json ... ' block.
          """
          match = re.search(r"json\n(.*?)\n", text, re.DOTALL)
          if match:
              return match.group(1)
          return text # Return original text if no markdown block found

  Ensure the uploaded_pdfs directory exists
      UPLOAD_DIR = "uploaded_pdfs"
      os.makedirs(UPLOAD_DIR, exist_ok=True)

      st.set_page_config(
          page_title="PDF Assistant",
          page_icon="📚",
          layout="wide",
          initial_sidebar_state="expanded"
      )

      st.sidebar.title("Upload your PDF")
      st.sidebar.markdown("Upload a PDF document to get a summary and generate quizzes.")

      uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

      st.title("📚 PDF Summarizer & Quiz Generator")
      st.markdown("Upload a PDF from the sidebar to get started.")

      file_path = None
      if uploaded_file:
          file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
          with open(file_path, "wb") as f:
              f.write(uploaded_file.getbuffer())

          st.sidebar.success(f"PDF '{uploaded_file.name}' uploaded successfully!")
          st.markdown(f"Loaded PDF: {uploaded_file.name}")

          st.subheader("📝 Document Summary")
          with st.spinner("Generating summary..."):
              try:
                  summary_result = Runner.run_sync(agent, f"Summarize the PDF located at {file_path}")
                  st.write(summary_result.final_output)
              except Exception as e:
                  st.error(f"Error generating summary: {e}")
                  st.info("Ensure GEMINI_API_KEY is set correctly and the agent can access the tool.")

          st.subheader("🧠 Quiz Generator")
          if st.button("Create Quiz", help="Generate an MCQ quiz from the uploaded PDF"):
              with st.spinner("Generating quiz... This might take a moment."):
                  try:
                      quiz_prompt = f"Using the 'create_quiz' tool, generate an MCQ style quiz from the PDF at {file_path}.Please   
      return only the quiz data as a JSON code block or a Python list of dictionaries."
                      quiz_result = Runner.run_sync(agent, quiz_prompt)

                      processed_output = extract_json_from_markdown(quiz_result.final_output)

                      try:
                          quiz_data = json.loads(processed_output)
                          st.success("Quiz generated successfully!")
                          for i, question_obj in enumerate(quiz_data):
                              st.markdown(f"---")
                              st.markdown(f"Question {i+1}: {question_obj['question']}")
                              options = question_obj.get('options', [])
                              if options:
                                  for option_idx, option in enumerate(options):
                                      st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;{chr(65+option_idx)}. {option}")

                              with st.expander(f"Show Answer for Question {i+1}"):
                                  st.info(f"Correct Answer: {question_obj.get('answer', 'N/A')}")
                      except json.JSONDecodeError:
                          try:
                              quiz_data = ast.literal_eval(processed_output)
                              st.success("Quiz generated successfully!")
                              for i, question_obj in enumerate(quiz_data):
                                  st.markdown(f"---")
                                  st.markdown(f"Question {i+1}: {question_obj['question']}")
                                  options = question_obj.get('options', [])
                                  if options:
                                      for option_idx, option in enumerate(options):
                                          st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;{chr(65+option_idx)}. {option}")

                                  with st.expander(f"Show Answer for Question {i+1}"):
                                      st.info(f"Correct Answer: {question_obj.get('answer', 'N/A')}")
                          except (ValueError, SyntaxError) as ast_error:
                              st.error("The agent returned output that could not be parsed as valid JSON or Python literal.")        
                              st.code(processed_output, language="text")
                              st.info(f"Parsing Error: {ast_error}. Please check the agent's output format.")
                  except Exception as e:
                      st.error(f"Error generating quiz: {e}")
                      st.info("Ensure GEMINI_API_KEY is set correctly and the agent can access the tool.")
      else:
          st.info("Upload a PDF and click 'Create Quiz' to generate questions.")
  else:
      st.info("Please upload a PDF file to begin.")
```

### Step 6: Dependency Management
   Create `requirements.txt` and install all necessary dependencies using `uv`.

1.  **Create `requirements.txt`:**
      touch requirements.txt
*Content for `requirements.txt`:*
      streamlit
      openai-agents
      pypdf2
      python-dotenv
2.  **Install dependencies:**
      uv pip install -r requirements.txt

## 5. Running and Testing the Application

1.  **Set your Gemini API Key:**
*   Open the `.env` file and replace `your_gemini_api_key_here` with your actual Gemini API key.
 *  **Note:** For this project, the summarization and quiz generation are placeholders. The `GEMINI_API_KEY` is primarily f
      the `openai-agents` SDK setup, but the LLM calls for actual summarization/quiz logic in `tools.py` are *not* implemented, so th
      key's functionality might not be fully tested in this placeholder version.

2.  **Run the Streamlit Application:**
*   Open your terminal in the project directory.
*   Execute:
          streamlit run app.py

*   A web browser window will open with the Streamlit app.

**Testing Scenarios:**
*   **Upload PDF:** Upload any PDF file via the sidebar. The summary section should display the first 1000 characters of the
     extracted text.
**Create Quiz:** Click the "Create Quiz" button. The quiz questions will appear in a formatted UI, with options and 
     expandable sections for answers.
**Observe Terminal Output:** Check your terminal for `--- summarize_pdf tool called ---` and `--- create_quiz tool calle
     ---` messages to confirm tool invocation.`