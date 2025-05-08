from flask import Flask, jsonify
from prediction import get_predictions

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Betwise Predictions"})

@app.route("/predictions")
def predictions():
    result = get_predictions()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)