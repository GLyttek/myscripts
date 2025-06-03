from groq import Groq
import os

# Initialize the Groq API using an environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

# Initialize the conversation list
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# Function to interact with the Groq model
def chat_with_groq(prompt, conversation):
    model_engine = "mixtral-8x7b-32768"
    
    # Add the new user message to the conversation list
    conversation.append({"role": "user", "content": prompt})
    
    # Generate a message from the model
    response = client.chat.completions.create(
        model=model_engine,
        messages=conversation
    )
    
    message_output = response.choices[0].message.content
    
    # Add the model's message to the conversation list
    conversation.append({"role": "assistant", "content": message_output})
    
    return message_output

# Main chat loop
if __name__ == "__main__":
    print("Chatbot initialized. Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye!")
            break
        else:
            bot_response = chat_with_groq(user_input, conversation)
            print(f"Chatbot: {bot_response}")
