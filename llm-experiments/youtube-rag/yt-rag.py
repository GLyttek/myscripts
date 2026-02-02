from flask import Flask, request, jsonify, render_template
from pytube import YouTube
from moviepy.editor import AudioFileClip
from faster_whisper import WhisperModel
import ollama
import torch
from sentence_transformers import SentenceTransformer, util
import os

app = Flask(__name__)

# Initialize OpenAI client
client = ollama.Client()

# Initialize SentenceTransformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Define system message
system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text."

# Function to read transcribed text from file
def read_transcribed_text(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            return file.read()
    else:
        return ""

# Function to get relevant context from the vault based on user input
def get_relevant_context(user_input, vault_embeddings, vault_content, model, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the user input
    input_embedding = model.encode([user_input])
    # Compute cosine similarity between the input and vault embeddings
    cos_scores = util.cos_sim(input_embedding, vault_embeddings)[0]
    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    video_url = request.form.get('https://www.youtube.com/shorts/4UJoL89QNdQ')
    video_path, error = download_youtube_video(video_url)
    if error:
        return jsonify({'error': error})

    mp3_file_path, error = convert_mp4_to_mp3(video_path, 'temp_audio.mp3')
    if error:
        return jsonify({'error': error})

    transcribed_text, error = transcribe_audio_to_text(mp3_file_path)
    if error:
        return jsonify({'error': error})

    return jsonify({'message': 'Transcription complete.', 'transcript': transcribed_text})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('user_message')
    conversation = [{"role": "system", "content": "Start of conversation"}]
    conversation.append({"role": "user", "content": user_message})

    response = client.chat(model="llama3", messages=conversation)  # Now using the correct method
    assistant_message = response['message']['content']
    
    return jsonify({'assistant_response': assistant_message})

if __name__ == '__main__':
    # Load vault content and embeddings
    vault_content = []
    if os.path.exists("vault.txt"):
        with open("vault.txt", "r", encoding='utf-8') as vault_file:
            vault_content = vault_file.readlines()

    vault_embeddings = model.encode(vault_content) if vault_content else []

    # Update the vault with transcribed text
    transcribed_text = read_transcribed_text("transcribed_text.txt")
    if transcribed_text:
        vault_content.append(transcribed_text)
        # Re-encode the vault embeddings
        vault_embeddings = model.encode(vault_content)

    app.run(debug=True)
