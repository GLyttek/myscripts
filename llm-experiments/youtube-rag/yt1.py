from flask import Flask, request, render_template_string
import torch
from sentence_transformers import SentenceTransformer, util
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='NA',
    timeout=660
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
vault_content = []
if os.path.exists("vault.txt"):
    with open("vault.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()

vault_embeddings = model.encode(vault_content) if vault_content else []
vault_embeddings_tensor = torch.tensor(vault_embeddings)

# Function to get relevant context from the vault based on user input
def get_relevant_context(user_input, vault_embeddings, vault_content, model, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the user input
    input_embedding=model.encode([user_input])
    # Compute cosine similarity between the input and vault embeddings
    cos_scores=util.cos_sim(input_embedding, vault_embeddings)[0]
    # Adjust top_k if it's greater than the number of available scores
    top_k=min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices=torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault
    relevant_context=[vault_content[idx].strip() for idx in top_indices]
    return relevant_context

# Function to read transcribed text from file
def read_transcribed_text(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            return file.read()
    else:
        return ""

# Update the vault with transcribed text
transcribed_text = read_transcribed_text("transcribed_text.txt")
if transcribed_text:
    vault_content.append(transcribed_text)
    # Re-encode the vault embeddings
    vault_embeddings = model.encode(vault_content)
    vault_embeddings_tensor = torch.tensor(vault_embeddings)

# Define the system message globally if it does not change
system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text."

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form['user_input']
        response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, model)
        return render_template_string(HTML_TEMPLATE, response=response, user_input=user_input)
    return render_template_string(HTML_TEMPLATE, response="", user_input="")

# Continue with the definition of ollama_chat and other necessary functions...
def ollama_chat(user_input, system_message, vault_embeddings, vault_content, model):
    relevant_context = get_relevant_context(user_input, vault_embeddings, vault_content, model)
    context_str = "\n".join(relevant_context) if relevant_context else "No relevant context found."

    user_input_with_context = user_input if not relevant_context else f"{context_str}\n\n{user_input}"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input_with_context}
    ]
    
    response = client.chat.completions.create(
        model="dolphin-llama3:latest",
        messages=messages
    )
    return response.choices[0].message.content


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Document Chat Interface</title>
</head>
<body>
    <h1>Chat with Ollama</h1>
    <form method="post">
        <textarea name="user_input" rows="4" cols="50">{{ user_input }}</textarea><br>
        <input type="submit" value="Ask Ollama">
    </form>
    <h2>Response:</h2>
    <p>{{ response }}</p>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
