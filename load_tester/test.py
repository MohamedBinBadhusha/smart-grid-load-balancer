import requests
import random
import time

# Load balancer endpoint
BALANCER_URL = "http://localhost:7000/route"

print("🔁 Sending charging requests to Load Balancer...\n")

for i in range(50):
    vehicle = {
        "vehicle_id": f"EV_{i+1}",
        "load": random.randint(1, 3)
    }
    try:
        response = requests.post(BALANCER_URL, json=vehicle)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Request {i+1} routed to {data['target_substation']} | Vehicle: {vehicle['vehicle_id']} | Load: {vehicle['load']}")
        else:
            print(f"❌ Request {i+1} failed: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Error on request {i+1}: {e}")
    time.sleep(0.2)  # Simulate light delay between EV arrivals
