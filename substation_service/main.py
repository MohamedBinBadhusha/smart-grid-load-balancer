from flask import Flask, request, jsonify
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading
import time
import random

app = Flask(__name__)

# Simulated current load
current_load = 0

# Prometheus metric
load_gauge = Gauge('substation_current_load', 'Current load at the substation')

@app.route('/charge', methods=['POST'])
def charge_vehicle():
    global current_load
    data = request.json
    vehicle_id = data.get("vehicle_id", "unknown")
    load = data.get("load", 1)

    current_load += load
    load_gauge.set(current_load)

    # Simulate charging
    def complete_charging():
        time.sleep(random.randint(3, 7))  # simulate 3–7 sec charging
        global current_load
        current_load -= load
        load_gauge.set(current_load)

    threading.Thread(target=complete_charging).start()

    return jsonify({"status": "charging started", "vehicle_id": vehicle_id, "load": load})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
