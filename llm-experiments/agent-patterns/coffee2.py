import time
import random
import torch
from transformers import LLaMAForConversational
import ollama 

model_name ="llama3"
llama_model=LLaMAForConversational.from_pretrained(model_name)

class Barista:
    def __init__(self, name, llama_model):
        self.name = name
        self.llama_model = llama_model

    def take_order(self, customer):
        print(f"{self.name} takes order from {customer.name}")
        response = self.llama_model.generate("What can I get started for you today?")
        print(f"{self.name}: {response}")

    def make_drink(self, customer, drink):
        print(f"{self.name} makes a {drink} for {customer.name}")
        time.sleep(random.randint(1, 3))  # simulate preparation time
        print(f"{self.name} hands {customer.name} a {drink}")

class Customer:
    def __init__(self, name, llama_model):
        self.name = name
        self.llama_model = llama_model

    def order(self, barista, drink):
        print(f"{self.name} orders a {drink} from {barista.name}")
        response = self.llama_model.generate(f"I'll have a {drink}, please.")
        print(f"{self.name}: {response}")
        barista.take_order(self)
        barista.make_drink(self, drink)

# Load a local instance of LLaMA
model_name = "llama-13b"
llama_model = LLaMAForConversational.from_pretrained(model_name)

# Create baristas and customers
barista1 = Barista("John", llama_model)
barista2 = Barista("Emily", llama_model)
customer1 = Customer("Alice", llama_model)
customer2 = Customer("Bob", llama_model)
customer3 = Customer("Charlie", llama_model)

# Customers order drinks
customer1.order(barista1, "latte")
customer2.order(barista2, "cappuccino")
customer3.order(barista1, "mocha")