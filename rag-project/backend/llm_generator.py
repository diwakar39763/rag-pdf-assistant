import ollama


def generate_answer(context, question, history=""):

    prompt = f"""
You are a helpful AI assistant.

Use the provided conversation history
and document context to answer.

Rules:
1. Use ONLY provided context.
2. If answer is missing, say:
   "I could not find the answer in the document."
3. Understand follow-up questions from history.

Conversation History:
{history}

Document Context:
{context}

Current Question:
{question}

Answer:
"""