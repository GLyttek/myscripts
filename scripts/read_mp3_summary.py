from faster_whisper import WhisperModel
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

def transcribe_audio(audio_path, model_size="medium"):
    model = WhisperModel(model_size, device="cpu")
    segments, _ = model.transcribe(audio_path)
    return " ".join([segment.text for segment in segments])

audio_file_path = os.getenv("AUDIO_FILE", "/path/to/your/mp3")
transcribed_text = transcribe_audio(audio_file_path)
with open("transcription.txt", "w") as file:
    file.write(transcribed_text)

def create_chat_completion(content):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": content}],
        model="mixtral-8x7b-32768",
    )
    return chat_completion.choices[0].message.content

def summarize_text(text):
    summary_request = "Summarize the following text:\n\n" + text
    return create_chat_completion(summary_request)

with open("transcription.txt", "r") as file:
    transcription = file.read()

summary = summarize_text(transcription)
with open("summary.txt", "w") as file:
    file.write(summary)

def generate_expert_opinion(summary, expert_type):
    opinion_request = f"Imagine you are an expert in {expert_type}. Provide a detailed analysis and your expert opinion on the following summary:\n\n{summary}"
    return create_chat_completion(opinion_request)

expert_types = ["science", "philosophy", "industry"]
opinions = {}
for expert in expert_types:
    opinions[expert] = generate_expert_opinion(summary, expert)

with open("expert_opinions.txt", "w") as file:
    for expert, opinion in opinions.items():
        file.write(f"Expert Opinion - {expert.title()}:\n{opinion}\n\n")
