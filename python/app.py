from flask import Flask, request, jsonify
import requests
from dcr_helpers import create_case, execute_event, get_enabled_events

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

@app.route("/available_actions", methods=["POST"])
def available_actions():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    role = data.get("role")  # "driver" or "passenger"
    bus_id = data.get("bus_id")
    passenger_id = data.get("passenger_id")

    if not case_id or not role:
        return "error: missing case_id or role", 400

    try:
        # Ask DCR engine for all enabled events
        enabled = get_enabled_events(case_id)  # helper in dcr_helpers

        if bus_id:
            role = "driver"
            role_events = [
                "ApproachStop",
                "PassStop",
                "ArriveAtStop",
                "RaiseEntrance",
                "StopProcess",
            ]
            siddhi_url = SIDDHI_INPUT_URL_DRIVER
        else:
            role = "passenger"
            role_events = [
                "StopBtnPressed",
                "SpecialBtnPress",
                "PassengersWaiting",
                "PassengersEnter",
                "PassengersExit"
            ]
            siddhi_url = SIDDHI_INPUT_URL_PASSENGER

        available = [e for e in enabled if e in role_events]

        # Build event for SIDDHI
        event = {
            "case_id": case_id,
            "role": role,
            "bus_id": bus_id,
            "passenger_id": passenger_id,
            "available_actions": available
        }

        requests.post(siddhi_url, json=event)
        return "success", 200

    except Exception as e:
        return f"error: {str(e)}", 400

@app.route("/create_case", methods=["POST"])
def create_case_route():
    data = request.get_json(force=True)
    bus_id = data.get("bus_id")

    if not bus_id:
        return jsonify({"error": "Missing required key: bus_id"}), 400

    try:
        # Call DCR helper to create a new case
        case_id = create_case()

        # Build event for SIDDHI
        event = {
            "bus_id": bus_id,
            "case_id": case_id,
            "action": "CreateCase"
        }

        # Send event to SIDDHI
        resp = requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)

        return "success", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/approach_stop", methods=["POST"])
def approach_stop():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    # Validate required fields
    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        result = execute_event(case_id, "ApproachStop")
        if result:
            # Build event for SIDDHI
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "ApproachStop"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)

            return "success", 200
        else:
            return "error: failed to execute event", 400
    except Exception as e:
        return f"error: {str(e)}", 400

@app.route("/special_btn_press", methods=["POST"])
def special_btn_press():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        result = execute_event(case_id, "SpecialBtnPress")
        if result:
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "SpecialBtnPress"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute event", 400
    except Exception as e:
        return f"error: {str(e)}", 400


@app.route("/passengers_waiting", methods=["POST"])
def passengers_waiting():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        result = execute_event(case_id, "PassengersWaiting")
        if result:
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "PassengersWaiting"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute event", 400
    except Exception as e:
        return f"error: {str(e)}", 400


@app.route("/stop_btn_pressed", methods=["POST"])
def stop_btn_pressed():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        result = execute_event(case_id, "StopBtnPressed")
        if result:
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "StopBtnPressed"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute event", 400
    except Exception as e:
        return f"error: {str(e)}", 400

@app.route("/arriving", methods=["POST"])
def arriving():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        # Try PassStop first
        if execute_event(case_id, "PassStop"):
            event_name = "PassStop"
        elif execute_event(case_id, "ArriveAtStop"):
            event_name = "ArriveAtStop"
        else:
            return "error: neither event could be executed", 400

        event = {
            "case_id": case_id,
            "bus_id": bus_id,
            "event": event_name
        }
        requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)

        return "success", 200

    except Exception as e:
        return f"error: {str(e)}", 400

@app.route("/check_bus_crowded", methods=["POST"])
def check_bus_crowded():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        result = execute_event(case_id, "CheckBusCrowded")
        if result:
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "CheckBusCrowded"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute CheckBusCrowded", 400
    except Exception as e:
        return f"error: {str(e)}", 400

@app.route("/open_doors", methods=["POST"])
def open_doors():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        if execute_event(case_id, "OpenDoors"):
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "OpenDoors"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute OpenDoors", 400
    except Exception as e:
        return f"error: {str(e)}", 400


@app.route("/close_doors", methods=["POST"])
def close_doors():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        if execute_event(case_id, "CloseDoors"):
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "CloseDoors"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute CloseDoors", 400
    except Exception as e:
        return f"error: {str(e)}", 400


@app.route("/deny_boarding", methods=["POST"])
def deny_boarding():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        if execute_event(case_id, "DenyBoarding"):
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "DenyBoarding"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute DenyBoarding", 400
    except Exception as e:
        return f"error: {str(e)}", 400

@app.route("/lower_entrance", methods=["POST"])
def lower_entrance():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        if execute_event(case_id, "LowerEntrance"):
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "LowerEntrance"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute LowerEntrance", 400
    except Exception as e:
        return f"error: {str(e)}", 400


@app.route("/raise_entrance", methods=["POST"])
def raise_entrance():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        if execute_event(case_id, "RaiseEntrance"):
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "RaiseEntrance"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute RaiseEntrance", 400
    except Exception as e:
        return f"error: {str(e)}", 400


@app.route("/depart_from_stop", methods=["POST"])
def depart_from_stop():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    bus_id = data.get("bus_id")

    if not case_id or not bus_id:
        return "error: missing case_id or bus_id", 400

    try:
        if execute_event(case_id, "DepartFromStop"):
            event = {
                "case_id": case_id,
                "bus_id": bus_id,
                "event": "DepartFromStop"
            }
            requests.post(SIDDHI_INPUT_URL_DRIVER, json=event)
            return "success", 200
        else:
            return "error: failed to execute DepartFromStop", 400
    except Exception as e:
        return f"error: {str(e)}", 400

@app.route("/passengers_enter", methods=["POST"])
def passengers_enter():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    passenger_id = data.get("passenger_id")

    if not case_id or not passenger_id:
        return "error: missing case_id or passenger_id", 400

    try:
        if execute_event(case_id, "PassengersEnter"):
            event = {
                "case_id": case_id,
                "passenger_id": passenger_id,
                "event": "PassengersEnter"
            }
            requests.post(SIDDHI_INPUT_URL_PASSENGER, json=event)
            return "success", 200
        else:
            return "error: failed to execute PassengersEnter", 400
    except Exception as e:
        return f"error: {str(e)}", 400


@app.route("/passengers_exit", methods=["POST"])
def passengers_exit():
    data = request.get_json(force=True)
    case_id = data.get("case_id")
    passenger_id = data.get("passenger_id")

    if not case_id or not passenger_id:
        return "error: missing case_id or passenger_id", 400

    try:
        if execute_event(case_id, "PassengersExit"):
            event = {
                "case_id": case_id,
                "passenger_id": passenger_id,
                "event": "PassengersExit"
            }
            requests.post(SIDDHI_INPUT_URL_PASSENGER, json=event)
            return "success", 200
        else:
            return "error: failed to execute PassengersExit", 400
    except Exception as e:
        return f"error: {str(e)}", 400





if __name__ == "__main__":
    app.run(port=5001, debug=True)