import streamlit as st
from langchain.chains import LLMChain
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Access the API key from the environment variable
api_key = os.environ.get("GEMINI_API_KEY")

# Global Prompt Templates
PROMPT_TEMPLATES = {
    "Product Backlog": """
    Based on the product description: "{input_text}",
    generate a high-level product backlog with at least 5 backlog items.
    Format: 
    - Backlog Item Title
    - Short Description
    """,
    "User Stories": """
    Based on the input "{input_text}",
    generate detailed user stories in the following format:
    - As a [role], I want to [action], so that [benefit].
    """,
    "Acceptance Criteria": """
    Based on the user story: "{input_text}",
    generate 3-5 clear acceptance criteria using the format:
    - [Criterion]
    """,
    "Definition of Ready (DoR)": """
    Provide a standard Definition of Ready (DoR) for agile user stories.
    """,
    "Definition of Done (DoD)": """
    Provide a standard Definition of Done (DoD) for agile user stories.
    """,
}

# Function to generate LLM response
def generate_response(prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
def main():
    st.title("Scaled Agile Assistant with Jira Export")
    st.sidebar.header("Tasks")
    task_type = st.sidebar.selectbox("Choose a Task", 
                                     ["Product Backlog", "User Stories", "Acceptance Criteria", 
                                      "Definition of Ready (DoR)", "Definition of Done (DoD)"])
    
    
    # Editable Prompt Template
    st.sidebar.header("Edit Prompt Template")
    template = st.sidebar.text_area("Prompt Template", PROMPT_TEMPLATES[task_type])
    PROMPT_TEMPLATES[task_type] = template

    # Main input area
    st.header(task_type)
    if task_type in ["Product Backlog", "User Stories", "Acceptance Criteria"]:
        input_text = st.text_area(f"Provide the {task_type.lower()} context:")
    else:
        input_text = None

    # Generate output
    if st.button("Generate"):
        with st.spinner("Generating..."):
            prompt = template.format(input_text=input_text)
            response = generate_response(prompt)
            st.success("Generated Output:")
            st.write(response)


    st.sidebar.header("About")
    st.sidebar.info("GenAI Assistant for Scaled Agile Framework with Jira Export.")

if __name__ == "__main__":
    main()
