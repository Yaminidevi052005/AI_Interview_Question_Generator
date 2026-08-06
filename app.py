from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader

import os
import streamlit as st


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API Key not found")
    st.stop()

client = Groq(api_key=api_key)


st.title("Interview Question Generator")

st.write("Welcome to the Interview Preparation App")


uploaded_resume = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)


resume_text = ""


if uploaded_resume is not None:

    pdf = PdfReader(uploaded_resume)

    for page in pdf.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    st.success("Resume uploaded successfully")


topic = st.text_input(
    "Enter the interview topic"
)


difficulty = st.selectbox(
    "Select Difficulty",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


number = st.number_input(
    "Number of Questions",
    min_value=1,
    max_value=20,
    value=5
)


if st.button("Generate Questions"):


    if uploaded_resume is None:
        st.warning("Please upload your resume first")
        st.stop()


    prompt = f"""
You are an interview preparation assistant.

Generate {number} {difficulty} level interview questions with expected answers.

Candidate Resume:
{resume_text}

Topic:
{topic}

Generate questions based on the candidate's resume and skills.
"""


    with st.spinner("Generating questions..."):

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


    questions = response.choices[0].message.content


    st.subheader("Generated Interview Questions")

    st.markdown(questions)