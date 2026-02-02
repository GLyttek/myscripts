import time
import random
import ollama

class Drink:
    def __init__(self, name, price, quality, options=None):
        self.name = name
        self.price = price
        self.quality = quality
        self.options = options or {}

    def customize(self, customizations):
        self.options.update(customizations)
        print(f"Customizing {self.name} with {customizations}")



# Function to interact with Ollama
def chat_with_ollama(prompt, conversation, role):
    model_engine = "dolphin-llama3:latest"
    # Add role to the conversation list for better context management
    conversation.append({"role": "user", "content": prompt, "speaker_role": role})
    
    response = ollama.chat(
        model=model_engine,
        messages=conversation
    )
    
    message_output = response['message']['content']
    # Append response with the role of the assistant (either 'barista' or 'customer')
    conversation.append({"role": "assistant", "content": message_output, "speaker_role": "ollama"})
    
    return message_output


class Barista:
    def __init__(self, name, conversation):
        self.name = name
        self.conversation = conversation

    def take_order(self, customer):
        print(f"{self.name} takes order from {customer.name}")
        response = chat_with_ollama(f"What can I get started for you today?", self.conversation)
        print(f"{self.name}: {response}")

    def make_drink(self, customer, drink):
        print(f"{self.name} makes a {drink} for {customer.name}")
        time.sleep(random.randint(1, 3))  # simulate preparation time
        print(f"{self.name} hands {customer.name} a {drink}")

class Customer:
    def __init__(self, name, money, personality):
        self.name = name
        self.money = money
        self.personality = personality
        self.mood = "neutral"
        self.conversation = []

    def order(self, barista, drink):
        if self.money >= drink.price:
            print(f"{self.name} orders a {drink.name} from {barista.name}")
            self.money -= drink.price
            barista.money += drink.price
            response = chat_with_ollama(f"I'll have a {drink.name}, please.", self.conversation)
            print(f"{self.name}: {response}")
            barista.take_order(self, drink)
        else:
            print(f"{self.name} can't afford a {drink.name}!")

class Barista:
    def __init__(self, name, money, personality):
        self.name = name
        self.money = money
        self.personality = personality
        self.mood = "neutral"
        self.conversation = []

    def take_order(self, customer, drink):
        print(f"{self.name} takes order from {customer.name}")
        response = chat_with_ollama(f"What can I get started for you today?", self.conversation)
        print(f"{self.name}: {response}")
        customer_response = chat_with_ollama(f"What would you like in your {drink.name}?", customer.conversation)
        print(f"{customer.name}: {customer_response}")
        self.make_drink(customer, drink, customer_response)

    def make_drink(self, customer, drink, customer_response):
        print(f"{self.name} makes a {drink.name} for {customer.name}")
        time.sleep(random.randint(1, 3))  # simulate preparation time
        print(f"{self.name} hands {customer.name} a {drink.name}")
        customer.mood = "happy" if drink.quality > 5 else "unhappy"

def chat_with_ollama(prompt, conversation):
    model_engine = "openchat:latest"
    conversation.append({"role": "user", "content": prompt})
    response = ollama.chat(
        model=model_engine,
        messages=conversation
    )
    message_output = response['message']['content']
    conversation.append({"role": "assistant", "content": message_output})
    return message_output

# Create customers and baristas
customer1 = Customer("Alice",30, "friendly")
customer2 = Customer("Bob", 150, "grumpy")
barista1 = Barista("John", 22, "sarcastic")
barista2 = Barista("Emily", 10, "friendly")

# Create drinks
latte = Drink("Latte", 5, 8)
cappuccino = Drink("Cappuccino", 6, 9)
mocha = Drink("Mocha", 7, 7)
latte.customize({"milk": "soy", "extra_shot": True})
# Simulate interactions
customer1.order(barista1, latte)
customer2.order(barista2, cappuccino)