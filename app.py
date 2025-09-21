import streamlit as st
import os
from PyPDF2 import PdfReader
import cohere

# Load Cohere API key from environment variable
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

st.title("Autonomous Career Advisor AI Agent with Chatbot")

# Upload resume as TXT or PDF
resume_file = st.file_uploader("Upload your resume (txt or pdf format)", type=["txt", "pdf"])

resume_text = ""
if resume_file is not None:
    if resume_file.type == "application/pdf":
        pdf_reader = PdfReader(resume_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"
    else:
        resume_text = resume_file.read().decode("utf-8")

    st.subheader("Uploaded Resume (text):")
    st.write(resume_text)

    # Pre-fill prompt with resume and instruction
    default_prompt = f"You are a career advisor. Review this resume and suggest improvements:\n{resume_text}"

    user_prompt = st.text_area("Or paste/edit your prompt:", value=default_prompt, height=200)

    if st.button("Send Chat Prompt"):
        if user_prompt.strip():
            with st.spinner("Generating response from the AI chatbot..."):
                response = co.chat(
                    message=user_prompt,
                    temperature=0.7,
                    max_tokens=300,
                )
                chat_output = response.text
            st.subheader("Chatbot Response:")
            st.write(chat_output)
        else:
            st.warning("Please enter a prompt to send.")
