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

class Food:
    def __init__(self, name, price):
        self.name = name
        self.price = price

def chat_with_ollama(prompt, conversation, role):
    model_engine = "granite3-moe:3b"
    conversation.append({"role": "user", "content": prompt, "speaker_role": role})

    response = ollama.chat(
        model=model_engine,
        messages=conversation
    )

    message_output = response['message']['content']
    conversation.append({"role": "assistant", "content": message_output, "speaker_role": "ollama"})

    return message_output

class Customer:
    def __init__(self, name, money, personality):
        self.name = name
        self.money = money
        self.personality = personality
        self.mood = "neutral"
        self.conversation = []

    def order(self, barista, item):
        if self.money >= item.price:
            interaction_prompt = f"{self.name} orders a {item.name} from {barista.name}."
            print(interaction_prompt)
            self.money -= item.price
            response = chat_with_ollama(f"Can I get a {item.name}? Also, what’s the special today?", self.conversation, "customer")
            print(f"{self.name}: {response}")
            barista.take_order(self, item, interaction_prompt)
        else:
            print(f"{self.name} can't afford a {item.name}!")
            self.mood = "frustrated"

class Barista:
    def __init__(self, name, money, personality):
        self.name = name
        self.money = money
        self.personality = personality
        self.mood = "neutral"
        self.conversation = []

    def take_order(self, customer, item, interaction_prompt=""):
        response = chat_with_ollama(f"{self.name}: Today's special is a homemade blueberry muffin. Would you like to add one to your order?", self.conversation, "barista")
        print(response)
        self.prepare_item(customer, item)

    def prepare_item(self, customer, item):
        try:
            preparation_prompt = f"{self.name} is preparing a {item.name} for {customer.name}, adding a little extra care today."
            print(preparation_prompt)
            time.sleep(random.randint(1, 2))
            handover_prompt = f"{self.name} hands {customer.name} a {item.name} with a smile."
            print(handover_prompt)
            customer.mood = "happy"
        except Exception as e:
            print(e)
            customer.mood = "frustrated"


# Initialize characters and items
customer1 = Customer("Alice", 30, "friendly")
customer2 = Customer("Bob", 150, "grumpy")
barista1 = Barista("John", 22, "sarcastic")
barista2 = Barista("Emily", 10, "friendly")

# Menu items
latte = Drink("Latte", 5, 8)
latte.customize({"milk": "soy", "extra_shot": True})
cappuccino = Drink("Cappuccino", 6, 9)
mocha = Drink("Mocha", 7, 7)
croissant = Food("Croissant", 3)

# Simulate interactions
customer1.order(barista1, latte)
customer2.order(barista2, croissant)
# Seasonal drink order
customer3 = Customer("Charlie", 45, "adventurous")
pumpkin_spice_latte = Drink("Pumpkin Spice Latte", 6, 9)
pumpkin_spice_latte.customize({"milk": "almond"})
customer3.order(barista1, pumpkin_spice_latte)

# Customer feedback and follow-up order
customer4 = Customer("Diana", 25, "curious")
espresso = Drink("Espresso", 3, 7)
customer4.order(barista2, espresso)  # Initial order
time.sleep(1)  # Wait time simulated for feedback
print(f"{customer4.name}: The espresso was a bit too strong last time. What do you recommend for something milder?")
chat_with_ollama("Can I have something less strong than an espresso?", customer4.conversation, "customer")
barista2.take_order(customer4, latte)  # Suggests a latte as a milder option

# Special request for allergies
customer5 = Customer("Evan", 40, "health-conscious")
gluten_free_muffin = Food("Gluten-Free Muffin", 4)
customer5.order(barista1, gluten_free_muffin)

# Multiple item order
customer6 = Customer("Fiona", 35, "busy")
coffee = Drink("Black Coffee", 2, 6)
bagel = Food("Bagel", 3)
customer6.order(barista2, coffee)
time.sleep(0.5)  # Simulate time before adding more to the order
customer6.order(barista2, bagel)

# Loyalty program interaction
customer7 = Customer("Greg", 30, "regular")
loyalty_cappuccino = Drink("Cappuccino", 6, 9)  # Assuming points sufficient for a free drink
print(f"{customer7.name}: I’d like to redeem my points for a free cappuccino, please.")
barista1.take_order(customer7, loyalty_cappuccino)
