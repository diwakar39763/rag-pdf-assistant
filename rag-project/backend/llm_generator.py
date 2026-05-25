import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(context, question, history=""):

    prompt = f"""
You are an AI assistant for question-answering.

Use the following context to answer the question.

Context:
{context}

Chat History:
{history}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content