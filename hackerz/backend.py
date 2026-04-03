from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import csv
import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
import threading

app = Flask(__name__)
CORS(app)

CSV_FILE = "tasks.csv"

EMAIL_USER = "mithiranarul007@gmail.com"
EMAIL_PASS = os.getenv("EMAIL_PASS")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

OLLAMA_URL = "http://localhost:11434/api/generate"

# =========================
# CREATE CSV
# =========================
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["topic", "date", "time", "status", "type", "email"])

# =========================
# EMAIL FUNCTION
# =========================
def send_email(to_email, subject, body):
    if not EMAIL_PASS:
        print("❌ EMAIL PASSWORD NOT SET")
        return

    msg = MIMEText(body)
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            print("✅ Email sent to", to_email)
    except Exception as e:
        print("❌ Email error:", e)

# =========================
# AI FUNCTIONS
# =========================
def generate_email(topic):
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": f"Write a professional email about {topic}",
        "stream": False
    })
    return response.json().get("response", "Error generating email")

def generate_reminder(topic):
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": f"Write a short reminder about {topic}",
        "stream": False
    })
    return response.json().get("response", "Error generating reminder")

# =========================
# MODERN FRONTEND UI
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Task Scheduler</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background: radial-gradient(circle at top, #0f172a, #020617);
            color: white;
            padding: 40px;
        }

        h1 {
            font-size: 40px;
            font-weight: 600;
            margin-bottom: 25px;
            background: linear-gradient(90deg, #38bdf8, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h3 {
            margin-bottom: 10px;
            font-weight: 400;
            color: #cbd5f5;
        }

        .glass {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            transition: 0.3s;
        }

        .glass:hover {
            transform: translateY(-3px);
            border-color: rgba(99,102,241,0.5);
        }

        input, select {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border-radius: 10px;
            border: none;
            outline: none;
            background: rgba(255,255,255,0.08);
            color: white;
        }

        input::placeholder {
            color: #94a3b8;
        }

        button {
            margin-top: 15px;
            padding: 12px;
            width: 100%;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            font-weight: 500;
            transition: 0.3s;
        }

        .add-btn {
            background: linear-gradient(90deg, #3b82f6, #6366f1);
            color: white;
        }

        .add-btn:hover {
            opacity: 0.85;
            transform: scale(1.02);
        }

        .delete-btn {
            background: #ef4444;
            color: white;
            margin-top: 10px;
        }

        .task-card {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .tag {
            font-size: 12px;
            padding: 4px 10px;
            border-radius: 999px;
            width: fit-content;
        }

        .pending {
            background: #facc15;
            color: black;
        }

        .done {
            background: #22c55e;
        }

        .meta {
            font-size: 13px;
            color: #94a3b8;
        }
    </style>
</head>

<body>

<h1>🚀 AI Task Scheduler</h1>

<div class="glass">
    <h3>Add Task</h3>

    <input id="topic" placeholder="Enter task topic...">
    <input type="date" id="date">
    <input type="time" id="time">

    <select id="type">
        <option value="email draft">📧 Email Draft</option>
        <option value="reminder">⏰ Reminder</option>
    </select>

    <input id="email" placeholder="Recipient email">

    <button class="add-btn" onclick="addTask()">Add Task</button>
</div>

<h3>📋 Tasks</h3>
<div id="tasks"></div>

<script>
async function addTask() {
    const topic = document.getElementById("topic");
    const date = document.getElementById("date");
    const time = document.getElementById("time");
    const type = document.getElementById("type");
    const email = document.getElementById("email");

    const task = {
        topic: topic.value,
        date: date.value,
        time: time.value,
        type: type.value,
        email: email.value
    };

    await fetch('/add-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task)
    });

    topic.value = "";
    date.value = "";
    time.value = "";
    email.value = "";

    loadTasks();
}

async function deleteTask(index) {
    await fetch('/delete-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index: index })
    });

    loadTasks();
}

async function loadTasks() {
    const res = await fetch('/tasks');
    const data = await res.json();

    let html = "";
    data.forEach((t, i) => {
        html += `
        <div class="glass task-card">
            <b>${t.topic}</b>

            <div class="meta">📅 ${t.date} • ⏰ ${t.time}</div>

            <div class="meta">🧠 ${t.type}</div>

            <div class="tag ${t.status === "done" ? "done" : "pending"}">
                ${t.status}
            </div>

            ${t.status === "done" ? 
                `<button class="delete-btn" onclick="deleteTask(${i})">Delete</button>` 
                : ""
            }
        </div>`;
    });

    document.getElementById("tasks").innerHTML = html;
}

loadTasks();
setInterval(loadTasks, 3000);
</script>

</body>
</html>
"""

# =========================
# ROUTES
# =========================
@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.json

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            data['topic'],
            data['date'],
            data['time'],
            "pending",
            data['type'],
            data['email']
        ])

    return jsonify({"message": "Task added"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with open(CSV_FILE, mode='r') as file:
        return jsonify(list(csv.DictReader(file)))

@app.route('/delete-task', methods=['POST'])
def delete_task():
    index = request.json.get("index")

    with open(CSV_FILE, mode='r') as file:
        rows = list(csv.reader(file))

    header = rows[0]
    data = rows[1:]

    if 0 <= index < len(data):
        data.pop(index)

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    return jsonify({"message": "Deleted"})

# =========================
# BACKGROUND LOOP
# =========================
def task_checker():
    while True:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        with open(CSV_FILE, mode='r') as file:
            rows = list(csv.DictReader(file))

        updated_rows = []

        for row in rows:
            task_time = datetime.strptime(row["time"], "%H:%M")
            current_time_obj = datetime.strptime(current_time, "%H:%M")

            if (
                row["status"] == "pending" and
                row["date"] == current_date and
                abs((current_time_obj - task_time).total_seconds()) < 60
            ):
                print("Processing:", row["topic"])

                if row["type"] == "email draft":
                    send_email(row["email"], row["topic"], generate_email(row["topic"]))
                else:
                    send_email(row["email"], "Reminder", generate_reminder(row["topic"]))

                row["status"] = "done"

            updated_rows.append(row)

        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["topic", "date", "time", "status", "type", "email"])
            writer.writeheader()
            writer.writerows(updated_rows)

        time.sleep(10)

# =========================
# START APP
# =========================
if __name__ == "__main__":
    threading.Thread(target=task_checker, daemon=True).start()
    app.run(port=5000)