from flask import Flask, jsonify, request

app = Flask(__name__)

HARDCODED_PASSWORD = "P@ssw0rd123"  # Pour le test Bandit

@app.route("/")
def index():
    return jsonify({"message": "Hello from Flassssk!"})

@app.route("/echo", methods=["POST"])
def echo():
    return jsonify({"you_sent": request.json})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
