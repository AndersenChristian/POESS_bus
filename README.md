# Movia – Event-Driven Transport System (Camunda 8 + Siddhi + DCR)

This project implements an event-driven architecture for Movia’s bus operations using:

- Camunda 8 (Zeebe) for BPMN orchestration  
- Siddhi (WSO2 Streaming Integrator) for real-time event processing  
- Python Flask microservice for integration  
- DCR Graphs for declarative stop-handling rules  

---

## Python Setup

The Python microservice runs the integration layer between Camunda and Siddhi.

### 1. Create virtual environment

    cd python
    python3 -m venv venv

# Activate
    source venv/bin/activate        # macOS/Linux
    venv\Scripts\activate           # Windows

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Run the microservice

    python app.py

---

## 🚀 Getting Started with Camunda and Siddhi

## 2. Start Siddhi Tooling (Editor)

Download Siddhi WSO2 Streaming Tooling 4.3.0 from:

    https://wso2.com/integration/wso2-streaming-integrator/

And place it in the `siddhi` folder.

Navigate to the tooling folder:

    cd siddhi/wso2si-tooling-4.3.0/bin
    ./tooling.sh

Open the browser UI:

    http://localhost:9390/editor

Use this editor to create and deploy Siddhi apps.

---

## 3. Start Siddhi Runtime

Download Siddhi WSO2 Streaming Integrator 4.3.1 from:

    https://wso2.com/integration/wso2-streaming-integrator/

And place it in the `siddhi` folder.

Navigate to the runtime folder:

    cd siddhi/wso2si-4.3.1/bin
    ./server.sh

Important ports:

- 7070 → HTTP input/output for Siddhi (@source/@sink)  
- 9390 → Siddhi tooling UI (from tooling.sh)  
- Other ports (9090, 9443, 7611, 7711) are internal and irrelevant  

Note: Siddhi Runtime has no graphical UI.  
Some SSL/Thrift warnings are normal.

---

## 4. Start Python Microservice

    cd python
    source venv/bin/activate
    export DCR_USERNAME={dcr_username}
    export DCR_PASSWORD={dcr_password}
    export DCR_GRAPH_ID={dcr_graph_id}
    python app.py

Default port:

    http://localhost:5001

Endpoints:

- `/camundaStream` → receives events from BPMN  
- `/siddhi/out` → receives events from Siddhi  

---

## 🟦 Summary

When everything is running:

- Camunda executes BPMN (“Transport Passengers”)  
- Siddhi processes real-time streams (traffic, weather, telemetry)  
- Python microservice connects BPMN ↔ Siddhi ↔ DCR  
- DCR models declare constraints on stop handling  

All components run locally and can be fully mocked for the project.
