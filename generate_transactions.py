# generate_transactions.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ---- Step 1: Define categories and merchants ----
categories = {
    "Groceries": ["Big Bazaar", "Reliance Fresh", "D-Mart", "More Supermarket"],
    "Dining": ["Dominos", "McDonald's", "Barbeque Nation", "Cafe Coffee Day"],
    "Transport": ["Uber", "Ola", "Rapido", "RedBus"],
    "Subscriptions": ["Netflix", "Spotify", "Amazon Prime", "Hotstar", "YouTube Premium"],
    "Utilities": ["Electricity Bill", "Water Bill", "Internet Bill", "Mobile Recharge"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Ajio"],
    "Rent": ["Apartment Rent"],
    "Healthcare": ["Pharmacy", "Doctor Visit", "Health Insurance"],
    "Entertainment": ["BookMyShow", "Gaming Purchase", "Theme Park"]
}

# ---- Step 2: Set time period ----
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)

# ---- Step 3: Generate random transactions ----
data = []
date = start_date

while date <= end_date:
    num_transactions = random.randint(1, 4)  # 1–4 transactions per day
    for _ in range(num_transactions):
        category = random.choice(list(categories.keys()))
        merchant = random.choice(categories[category])

        # Random amount logic
        if category == "Rent":
            amount = round(random.uniform(8000, 20000), 2)
        elif category == "Utilities":
            amount = round(random.uniform(300, 1500), 2)
        elif category == "Subscriptions":
            amount = random.choice([199, 299, 499, 899])
        elif category == "Transport":
            amount = round(random.uniform(100, 700), 2)
        else:
            amount = round(random.uniform(150, 5000), 2)

        data.append([date.strftime('%Y-%m-%d'), merchant, category, amount])

    date += timedelta(days=1)

# ---- Step 4: Create DataFrame ----
df = pd.DataFrame(data, columns=["Date", "Merchant", "Category", "Amount"])

# ---- Step 5: Add synthetic Payment Method and Account Balance ----
payment_methods = ["Credit Card", "Debit Card", "UPI", "Wallet"]
df["Payment_Method"] = [random.choice(payment_methods) for _ in range(len(df))]
df["Account_Balance"] = np.maximum(
    0, np.random.normal(loc=50000, scale=15000, size=len(df)).round(2)
)

# ---- Step 6: Save to CSV ----
df.to_csv("transactions.csv", index=False)
print("✅ transactions.csv generated successfully with", len(df), "records!")
print(df.head())
