import streamlit as st
import os
import json
import re
import ast
from agent import agent
from agents import Runner

# -----------------------------------------------------------
# Helper: Extract JSON from agent output (markdown or raw text)
# -----------------------------------------------------------
def extract_json_from_markdown(text: str) -> str:
    """
    Extract JSON from a Markdown ```json code block``` OR
    fallback to extracting between the first [ and last ].
    """
    code_block = re.search(r"```json\s*(.*?)```", text, re.DOTALL)
    if code_block:
        return code_block.group(1).strip()

    first_bracket = text.find('[')
    last_bracket = text.rfind(']')

    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        return text[first_bracket:last_bracket + 1].strip()

    return text.strip()


# -----------------------------------------------------------
# Setup
# -----------------------------------------------------------
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("📄 Upload your PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

st.title("📚 PDF Summarizer & Quiz Generator")
st.markdown("Upload a PDF from the sidebar to begin.")

file_path = None

# -----------------------------------------------------------
# Save uploaded PDF
# -----------------------------------------------------------
if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success(f"PDF '{uploaded_file.name}' uploaded successfully!")
    st.markdown(f"### 📄 Loaded PDF: **{uploaded_file.name}**")

    # -----------------------------------------------------------
    # Summary
    # -----------------------------------------------------------
    st.subheader("📝 Document Summary")
    with st.spinner("Generating summary..."):
        try:
            summary_result = Runner.run_sync(agent, f"Summarize the PDF located at {file_path}")
            st.write(summary_result.final_output)
        except Exception as e:
            st.error(f"Error generating summary: {e}")
            st.info("Check GEMINI_API_KEY and tool configuration.")

    # -----------------------------------------------------------
    # Quiz Generator
    # -----------------------------------------------------------
    st.subheader("🧠 Quiz Generator")

    if st.button("Create Quiz"):
        with st.spinner("Generating quiz..."):

            try:
                quiz_prompt = (
                    f"Use the 'create_quiz' tool to generate an MCQ quiz from the PDF at {file_path}. "
                    "Return ONLY the quiz as a JSON list or a markdown JSON code block. "
                    "Format: [{'question': '...', 'options': [...], 'answer': '...'}]"
                )

                quiz_result = Runner.run_sync(agent, quiz_prompt)

                processed_output = extract_json_from_markdown(quiz_result.final_output)

            except Exception as e:
                st.error(f"Agent Error: {e}")
                st.stop()

            # -----------------------------------------------------------
            # Parse JSON
            # -----------------------------------------------------------
            try:
                quiz_data = json.loads(processed_output)
            except json.JSONDecodeError:
                try:
                    quiz_data = ast.literal_eval(processed_output)
                except Exception as err:
                    st.error("❌ Could not parse the quiz output.")
                    st.code(processed_output)
                    st.info(f"Parsing Error: {err}")
                    st.stop()

            # -----------------------------------------------------------
            # Display Quiz
            # -----------------------------------------------------------
            st.success("✅ Quiz generated successfully!")

            for i, q in enumerate(quiz_data):
                st.markdown("---")
                st.markdown(f"### **Q{i+1}. {q['question']}**")

                for idx, opt in enumerate(q.get("options", [])):
                    st.write(f"{chr(65+idx)}. {opt}")

                with st.expander(f"Show Answer for Question {i+1}"):
                    st.info(f"**Correct Answer:** {q.get('answer', 'N/A')}")

else:
    st.info("⬅️ Upload a PDF to generate summary and quiz.")
