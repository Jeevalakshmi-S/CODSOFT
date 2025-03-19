from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # Allow frontend to talk to backend

tasks = []  # Store tasks in memory

@app.route('/')
def home():
    return render_template('index.html')  # Serve the frontend

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)  # Return all tasks

@app.route('/add', methods=['POST'])
def add_task():
    data = request.json
    task = data.get('task')
    if task:
        tasks.append(task)
        return jsonify({"message": "Task added"}), 201
    return jsonify({"error": "No task provided"}), 400

@app.route('/delete/<int:index>', methods=['DELETE'])
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Invalid index"}), 400

if __name__ == '__main__':
    app.run(debug=True)
