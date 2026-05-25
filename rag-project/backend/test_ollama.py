import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {
            'role': 'user',
            'content': 'Explain AI in simple words'
        }
    ]
)

print(response['message']['content'])