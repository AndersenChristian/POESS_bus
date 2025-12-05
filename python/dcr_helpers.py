import os
import base64
import requests
import re

import xml.dom.minidom


# Base API URL
DCR_API_BASE = "https://repository.dcrgraphs.net/api"

# Credentials and graph ID (set via environment variables or hardcode for testing)
USERNAME = os.getenv("DCR_USERNAME", "your_username")
PASSWORD = os.getenv("DCR_PASSWORD", "your_password")
DCR_GRAPH_ID = os.getenv("DCR_GRAPH_ID", "your_graph_id")

# Prepare Basic Auth header
auth_string = f"{USERNAME}:{PASSWORD}"
b64_auth = base64.b64encode(auth_string.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {b64_auth}",
    "Accept": "application/xml",
    "Content-Type": "application/json"
}

def create_case():
    """
    Create a new simulation (case) for the given graph.
    Returns the case ID if successful.
    """
    create_url = f"{DCR_API_BASE}/graphs/{DCR_GRAPH_ID}/sims"
    r = requests.post(create_url, headers=HEADERS, json={})
    print(f"[Create Case] {r.status_code}")

    if r.status_code not in (200, 201):
        print("Failed to create case.")
        return None

    # Fetch all sims and extract the latest case ID
    sims_url = f"{DCR_API_BASE}/graphs/{DCR_GRAPH_ID}/sims?filter=all"
    r2 = requests.get(sims_url, headers=HEADERS)
    xml = r2.text

    # Regex to extract trace IDs: <trace id="12345">
    ids = re.findall(r'<trace[^>]*id="(\d+)"', xml)
    if not ids:
        print("No case IDs found!")
        print(xml)
        return None

    case_id = ids[-1]
    print("New CASE ID =", case_id)
    return case_id

def get_enabled_events(case_id):
    """
    Return list of enabled & pending event IDs for a given case.
    """
    url = f"{DCR_API_BASE}/graphs/{DCR_GRAPH_ID}/sims/{case_id}/events"
    r = requests.get(url, headers=HEADERS)
    xml = r.text.replace('\\"', '"')

    # Regex to find events with enabled="true" and pending="true"
    pattern = r'<event[^>]*id="([^"]+)"[^>]*enabled=\"true\"'
    #patern = r ’< event [^ >]* id =\\"?([^\\"]+) \\"?[^ >]* enabled =\\"? true\\"?[^ >]* pending =\\"? true \\"?’
    events = re.findall(pattern, xml)

    print("raw xml:", xml)
    print("Detected pending events:", events)
    return events

def execute_event(case_id, event_id):
    """
    Execute a DCR event by ID.
    """
    url = f"{DCR_API_BASE}/graphs/{DCR_GRAPH_ID}/sims/{case_id}/events/{event_id}"
    r = requests.post(url, headers=HEADERS, json={})
    print(f"[Execute {event_id}] => {r.status_code}")
    return r.status_code

