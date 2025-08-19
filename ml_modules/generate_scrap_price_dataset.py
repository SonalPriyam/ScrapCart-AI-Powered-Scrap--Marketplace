import pandas as pd
import numpy as np
import random

scrap_types = ["Metal", "Plastic", "Paper", "Glass", "Clothes", "E waste", "Others"]
conditions = ["New", "Used", "Recyclable", "Damaged", "Other"]
cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Pune", "Ahmedabad", "Lucknow", "Jaipur"]
base_prices = {
    "Metal": (28, 60),
    "Plastic": (10, 20),
    "Paper": (6, 12),
    "Glass": (15, 28),
    "Clothes": (5, 16),
    "E waste": (40, 75),
    "Others": (8, 35)
}

data = []
for _ in range(3000):
    scrap_type = random.choice(scrap_types)
    condition = random.choice(conditions)
    location = random.choice(cities)
    quantity = random.randint(5, 150)
    base_min, base_max = base_prices[scrap_type]
    price = np.random.uniform(base_min, base_max)
    if condition == "New":
        price *= 1.30
    elif condition == "Damaged":
        price *= 0.65
    elif condition == "Recyclable":
        price *= 1.10
    elif condition == "Used":
        price *= 0.9
    if quantity > 70:
        price *= 0.93
    expected_price = max(4, round(price, 2))
    data.append({
        "scrap_type": scrap_type,
        "quantity": quantity,
        "location": location,
        "condition": condition,
        "expected_price": expected_price
    })

df = pd.DataFrame(data)
df.to_csv("ml_modules/scrap_price_dataset.csv", index=False)
print("Generated 3000 rows in ml_modules/scrap_price_dataset.csv")
