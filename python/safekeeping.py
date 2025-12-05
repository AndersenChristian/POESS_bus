from flask import Flask, request, jsonify
import requests
from dcr_helpers import create_case, execute_event

from enum import Enum

class EventID(str, Enum):
    ApproachStop = "ApproachStop"
    PassStop = "PassStop"
    StopProcess = "StopProcess"
    RaiseEntrance = "RaiseEntrance"
    PassengersExit = "PassengersExit"
    LowerEntrance = "LowerEntrance"
    OpenDoors = "OpenDoors"
    ArriveAtStop = "ArriveAtStop"
    CheckBusCrowded = "CheckBusCrowded"
    DenyBoarding = "DenyBoarding"
    PassengersEnter = "PassengersEnter"
    CloseDoors = "CloseDoors"
    DepartFromStop = "DepartFromStop"
    SpecialBtnPress = "SpecialBtnPress"
    PassengersWaiting = "PassengersWaiting"
    StopBtnPressed = "StopBtnPressed"


app = Flask(__name__)

# --- Siddhi endpoints ---
SIDDHI_INPUT_URL_DRIVER = "http://localhost:7071/driver"  # Where we send events to Siddhi
SIDDHI_INPUT_URL_PASSENGER = "http://localhost:7072/passenger"  # Where we send events to Siddhi

# --- Helper functions to ensure correct JSON format ---
def format_driver_event(driverId, busId, action):
    return {"driverId": driverId, "busId": busId, "action": action}

def format_passenger_event(passengerId, busId, action):
    return {"passengerId": passengerId, "busId": busId, "action": action}


# --- Input endpoints: receive events from external clients/BPMN ---
@app.route("/driver", methods=["POST"])
def driver_event():
    data = request.json
    # Validate required keys
    if not all(k in data for k in ("driverId", "busId", "action")):
        return jsonify({"error": "Missing required keys"}), 400
    # Forward to Siddhi
    resp = requests.post(SIDDHI_INPUT_URL_DRIVER, json=format_driver_event(
        data["driverId"], data["busId"], data["action"]
    ))
    return jsonify({"status": "forwarded", "siddhi_status": resp.status_code}), 200

@app.route("/passenger", methods=["POST"])
def passenger_event():
    data = request.json
    # Validate required keys
    if not all(k in data for k in ("passengerId", "busId", "action")):
        return jsonify({"error": "Missing required keys"}), 400
    # Forward to Siddhi
    resp = requests.post(SIDDHI_INPUT_URL_PASSENGER, json=format_passenger_event(
        data["passengerId"], data["busId"], data["action"]
    ))
    return jsonify({"status": "forwarded", "siddhi_status": resp.status_code}), 200


# --- Output endpoint: receive events from Siddhi ---
# Driver sink endpoint
@app.route('/driver/<driverId>', methods=['POST'])
def driver_sink(driverId):
    data = request.get_json(force=True)
    print(f"Driver sink called for driverId={driverId}")
    print("Payload received:", data)
    return jsonify({"status": "ok"}), 200

# Passenger sink endpoint (by passengerId)
@app.route('/passenger_id/<passengerId>', methods=['POST'])
def passenger_sink(passengerId):
    data = request.get_json(force=True)
    print(f"Passenger sink called for passengerId={passengerId}")
    print("Payload received:", data)
    return jsonify({"status": "ok"}), 200

# Passenger notification sink endpoint (by busId)
@app.route('/passenger_bus/<busId>', methods=['POST'])
def passenger_notification_sink(busId):
    data = request.get_json(force=True)
    print(f"Passenger notification sink called for busId={busId}")
    print("Payload received:", data)
    return jsonify({"status": "ok"}), 200

@app.route('/getBusStateResponse', methods=['POST'])
def getAllBusses():
    data = request.get_json(force=True)
    print("got all busses")
    print("Payload received:", data)
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)