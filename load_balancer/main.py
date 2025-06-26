from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

# Substation endpoints
SUBSTATIONS = {
    "subA": "http://substation1:8000",
    "subB": "http://substation2:8000"
}

# Store substation loads
current_loads = {name: float("inf") for name in SUBSTATIONS}

# Background task to fetch substation load from /metrics
def update_substation_loads():
    while True:
        for name, url in SUBSTATIONS.items():
            try:
                response = requests.get(f"{url}/metrics")
                for line in response.text.splitlines():
                    if "substation_current_load" in line and not line.startswith("#"):
                        load_value = float(line.split()[-1])
                        current_loads[name] = load_value
            except Exception:
                current_loads[name] = float("inf")
        time.sleep(2)

@app.route('/route', methods=['POST'])
def handle_request():
    vehicle_data = request.json
    # Choose substation with least current load
    best_sub = min(current_loads, key=current_loads.get)
    target_url = f"{SUBSTATIONS[best_sub]}/charge"

    try:
        sub_response = requests.post(target_url, json=vehicle_data)
        return jsonify({
            "status": "redirected",
            "target_substation": best_sub,
            "substation_reply": sub_response.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start background thread
    threading.Thread(target=update_substation_loads, daemon=True).start()
    app.run(host='0.0.0.0', port=7000)
