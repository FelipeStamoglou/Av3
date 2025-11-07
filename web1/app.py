from flask import Flask, jsonify
import time

app = Flask(__name__)

SERVICE_NAME = "web1"

@app.route("/")
def index():
    return jsonify({
        "client_ip": "simulated",
        "latency": 1e-6,
        "server": SERVICE_NAME,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
