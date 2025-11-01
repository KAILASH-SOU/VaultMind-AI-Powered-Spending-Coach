# inject_scenario.py
from simulator_stream import append_csv, random_transaction
from datetime import datetime

# Duplicate subscription
append_csv(random_transaction(forced={"category":"Subscriptions","merchant":"Netflix","amount":499}, date=datetime.now()))
append_csv(random_transaction(forced={"category":"Subscriptions","merchant":"Netflix","amount":499}, date=datetime.now()))
print("Injected duplicate subscription")

# Big spike
append_csv(random_transaction(forced={"category":"Shopping","merchant":"Amazon","amount":25000}, date=datetime.now()))
print("Injected big spike")
