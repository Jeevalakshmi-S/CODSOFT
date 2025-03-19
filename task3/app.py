from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# JSON file to store contacts
CONTACTS_FILE = "contacts.json"

# Function to read contacts from file
def read_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contacts", methods=["GET"])
def get_contacts():
    return jsonify(read_contacts())

@app.route("/add", methods=["POST"])
def add_contact():
    data = request.json
    contacts = read_contacts()
    
    new_contact = {
        "name": data["name"],
        "phone": data["phone"],
        "email": data["email"],
        "address": data["address"]
    }
    contacts.append(new_contact)
    save_contacts(contacts)
    return jsonify({"message": "Contact added successfully!"})

@app.route("/update", methods=["POST"])
def update_contact():
    data = request.json
    contacts = read_contacts()

    for contact in contacts:
        if contact["phone"] == data["old_phone"]:
            contact["name"] = data["name"]
            contact["phone"] = data["phone"]
            contact["email"] = data["email"]
            contact["address"] = data["address"]
            save_contacts(contacts)
            return jsonify({"message": "Contact updated successfully!"})

    return jsonify({"error": "Contact not found!"}), 404

@app.route("/delete", methods=["POST"])
def delete_contact():
    data = request.json
    contacts = read_contacts()
    contacts = [c for c in contacts if c["phone"] != data["phone"]]
    save_contacts(contacts)
    return jsonify({"message": "Contact deleted successfully!"})

@app.route("/search", methods=["POST"])
def search_contact():
    data = request.json
    contacts = read_contacts()
    query = data["query"].lower()
    
    results = [c for c in contacts if query in c["name"].lower() or query in c["phone"]]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
