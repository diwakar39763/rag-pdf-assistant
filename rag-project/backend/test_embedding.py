from embedding_generator import generate_embedding

text = "Quantum computing uses qubits"

embedding = generate_embedding(text)

print("Embedding Length:", len(embedding))

print("\nFirst 10 Values:\n")

print(embedding[:10])