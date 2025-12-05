from flask import Flask, request

app = Flask(__name__)

@app.route("/driver", methods=["POST"])
def driver():
    print("Driver event:", request.json)
    return "ok"

@app.route("/passenger", methods=["POST"])
def passenger():
    print("Passenger event:", request.json)
    return "ok"

app.run(port=7071)  # run one instance for driver
# run another instance on port 7072 for passenger
