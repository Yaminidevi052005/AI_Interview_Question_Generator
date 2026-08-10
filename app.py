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

# Phase 2 - Skill Gap Analysis

required_skills = st.text_area(
    "Enter required skills given in the job description"
)

if st.button("Analyze Skill Gap"):

    if uploaded_resume is None:
        st.warning("Upload your resume")
        st.stop()

    if not required_skills:
        st.warning("Enter required skills given in the job description")
        st.stop()

    prompt = f"""
You are an Interview Preparation Assistant.

Compare the resume with the required skills.

Resume:
{resume_text}

Required Skills:
{required_skills}

IMPORTANT:
The final answer MUST contain an
"OVERALL SKILL MATCH PERCENTAGE".

Calculate it using:

(Number of Matched Skills / Total Number of Required Skills) × 100

Give ONE overall percentage only.
Do not give separate percentages for individual skills.

Give the result ONLY in this format:

MATCHED SKILLS:
- skill 1
- skill 2
- skill 3

MISSING SKILLS:
- skill 1
- skill 2

OVERALL SKILL MATCH PERCENTAGE:
OVERALL SKILL MATCH:
Calculate the percentage using this formula:

Overall Skill Match Percentage =
(Number of Matched Skills / Total Number of Required Skills) × 100

You MUST provide one final percentage.
Example: Overall Skill Match Percentage: 60%

Do not omit this percentage.
Do not give separate percentages for individual skills.

LEARNING SUGGESTIONS:
- Missing skill → what to learn
- Missing skill → what to practice

7-DAY ROADMAP:
Day 1: Topic → Practice
Day 2: Topic → Practice
Day 3: Topic → Practice
Day 4: Topic → Practice
Day 5: Topic → Practice
Day 6: Topic → Practice
Day 7: Topic → Practice

Rules:
- Use short bullet points only.
- Do NOT write paragraphs.
- Do NOT add long explanations.
- Keep every point to one short sentence.
- Give suggestions only for missing skills.
- Keep the 7-day roadmap practical and concise.
- Do not omit the overall skill match percentage.
- Give the 7 day learning roadmap as bullet points(line by line).
- Suggest the user to learn the skill perfectly which is mentioned as basic in the resume.
- The learning suggestions should be user friendly and it should not be in a one line.
- Suggest the to prepare for the interview based on the given roadmap.
"""

    with st.spinner("Analyzing skill gap..."):

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    skill_analysis = response.choices[0].message.content

    st.subheader("Skill Gap Analysis")

    st.markdown(skill_analysis)

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