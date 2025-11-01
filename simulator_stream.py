# simulator_stream.py
import csv
import time
import random
from datetime import datetime, timedelta

MERCHANTS = {
    "Groceries": ["Big Bazaar", "Reliance Fresh", "D-Mart"],
    "Subscriptions": ["Netflix", "Spotify", "Prime"],
    "Dining": ["Dominos", "Cafe Coffee Day", "McDonald's"],
    "Transport": ["Uber", "Ola"],
    "Shopping": ["Amazon", "Flipkart"]
}

PAYMENTS = ["Credit Card", "Debit Card", "UPI", "Wallet"]

def random_transaction(date=None, forced=None):
    if forced:
        # forced is a dict with keys: category, merchant, amount
        category = forced.get("category")
        merchant = forced.get("merchant")
        amount = forced.get("amount")
    else:
        category = random.choice(list(MERCHANTS.keys()))
        merchant = random.choice(MERCHANTS[category])
        if category == "Subscriptions":
            amount = random.choice([99, 199, 299, 499])
        else:
            amount = round(random.uniform(50, 4000), 2)
    return {
        "Date": (date or datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "Merchant": merchant,
        "Category": category,
        "Amount": amount,
        "Payment_Method": random.choice(PAYMENTS),
        "Account_Balance": round(random.uniform(10000, 80000), 2)
    }

def append_csv(row, filename="transactions.csv"):
    header = ["Date","Merchant","Category","Amount","Payment_Method","Account_Balance"]
    write_header = False
    try:
        with open(filename, "r", newline="") as f:
            pass
    except FileNotFoundError:
        write_header = True
    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

if __name__ == "__main__":
    print("Starting simulator. Press Ctrl+C to stop.")
    # Example: first seed with a few days of normal transactions
    start = datetime.now() - timedelta(days=30)
    for d in range(30):
        for _ in range(random.randint(1,3)):
            row = random_transaction(date=start + timedelta(days=d))
            append_csv(row)
    print("Seeded 30 days of data.")
    # Then stream new transactions every 5 seconds
    try:
        counter = 0
        while True:
            # Inject special events at certain times (demo scenarios)
            counter += 1
            if counter == 5:
                # duplicate subscription scenario: two subscription charges same day
                r1 = random_transaction(forced={"category":"Subscriptions","merchant":"Netflix","amount":499})
                r2 = random_transaction(forced={"category":"Subscriptions","merchant":"Netflix","amount":499})
                append_csv(r1)
                append_csv(r2)
                print("Injected duplicate subscription.")
            elif counter == 12:
                # big spike scenario
                r = random_transaction(forced={"category":"Shopping","merchant":"Amazon","amount":25000})
                append_csv(r)
                print("Injected big spike.")
            else:
                row = random_transaction()
                append_csv(row)
            time.sleep(5)  # adjust for demo speed
    except KeyboardInterrupt:
        print("Simulator stopped.")
