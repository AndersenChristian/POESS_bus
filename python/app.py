from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Change this if Siddhi runs on another machine
SIDDHI_URL = "http://localhost:7071/gps"

@app.route("/camundaStream", methods=["POST"])
def camunda_stream():
    data = request.json
    print("📥 Received from BPMN:", data)

    # Forward to Siddhi
    resp = requests.post(SIDDHI_URL, json=data)
    print("➡️ Forwarded to Siddhi:", resp.status_code)

    return jsonify({"status": "ok"}), 200

@app.route("/siddhi/out", methods=["POST"])
def siddhi_out():
    data = request.json
    print("📤 Received from Siddhi:", data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
