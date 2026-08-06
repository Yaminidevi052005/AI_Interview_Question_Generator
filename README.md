# AI Interview Question Generator

## Project Overview

AI Interview Question Generator is an AI-based application that generates personalized interview questions based on the candidate's resume and selected topic using Groq AI.

## Features

- Upload resume in PDF format
- Extract resume content
- Generate resume-based interview questions
- Select difficulty level
- Generate questions with expected answers

## Technologies Used

- Python
- Streamlit
- Groq API
- PyPDF
- Python-dotenv

## Workflow

1. Upload resume PDF
2. Extract resume details
3. Select topic and difficulty level
4. Generate AI-based interview questions

## Installation

Install dependencies:

pip install -r requirements.txt

## Environment Setup

Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here

##Run Application

Start the Streamlit application:

```bash
streamlit run app.py

## Future Enhancements

- AI-based answer evaluation
- Mock interview chatbot
- Interview performance scoring
- Download generated questions as PDF

