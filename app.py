from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

FILE = "data.json"

# Ensure file exists
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

def read_data():
    with open(FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return jsonify({"message": "Notes API running"})

@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(read_data())

@app.route("/notes", methods=["POST"])
def add_note():
    data = read_data()
    note = request.json

    if not note or "text" not in note:
        return {"error": "Invalid input"}, 400

    data.append(note)
    write_data(data)

    return {"message": "Note added", "data": note}

@app.route("/notes/<int:index>", methods=["DELETE"])
def delete_note(index):
    data = read_data()

    if index >= len(data):
        return {"error": "Note not found"}, 404

    removed = data.pop(index)
    write_data(data)

    return {"message": "Deleted", "data": removed}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)