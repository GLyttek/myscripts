import time
import random

class Barista:
    def __init__(self, name):
        self.name = name

    def take_order(self, customer):
        print(f"{self.name} takes order from {customer.name}")

    def make_drink(self, customer, drink):
        print(f"{self.name} makes a {drink} for {customer.name}")
        time.sleep(random.randint(1, 3))  # simulate preparation time
        print(f"{self.name} hands {customer.name} a {drink}")

class Customer:
    def __init__(self, name):
        self.name = name

    def order(self, barista, drink):
        print(f"{self.name} orders a {drink} from {barista.name}")
        barista.take_order(self)
        barista.make_drink(self, drink)

# Create baristas and customers
barista1 = Barista("John")
barista2 = Barista("Emily")
customer1 = Customer("Alice")
customer2 = Customer("Bob")
customer3 = Customer("Charlie")

# Customers order drinks
customer1.order(barista1, "latte")
customer2.order(barista2, "cappuccino")
customer3.order(barista1, "mocha")