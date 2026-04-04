from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import csv
import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# =========================
# CONFIG (SECURE via setx)
# =========================
CSV_FILE = "tasks.csv"

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"

if not EMAIL_USER or not EMAIL_PASS or not SARVAM_API_KEY:
    raise ValueError("❌ Set environment variables using setx first!")

# =========================
# CREATE CSV
# =========================
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["topic", "date", "time", "status", "type", "email"])

# =========================
# EMAIL FUNCTION
# =========================
def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print("✅ Email sent")

    except Exception as e:
        print("❌ Email error:", e)

# =========================
# SARVAM AI
# =========================
def generate_text(prompt):
    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sarvam-m",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(SARVAM_URL, headers=headers, json=data)

        if response.status_code != 200:
            return "AI error"

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)

# =========================
# TASK SCHEDULER
# =========================
def task_scheduler():
    while True:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        with open(CSV_FILE, 'r') as f:
            rows = list(csv.DictReader(f))

        updated_rows = []

        for row in rows:
            task_time = datetime.strptime(row["time"], "%H:%M")
            current_time_obj = datetime.strptime(current_time, "%H:%M")

            if (
                row["status"] == "pending" and
                row["date"] == current_date and
                task_time <= current_time_obj
            ):
                print("🚀 Running:", row["topic"])

                if row["type"] == "email draft":
                    body = generate_text(f"Write a professional email about {row['topic']}")
                    send_email(row["email"], row["topic"], body)

                elif row["type"] == "reminder":
                   body = f"Reminder: Do the work - {row['topic']}"
                   send_email(row["email"], "Reminder", body)

                row["status"] = "done"

            updated_rows.append(row)

        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["topic","date","time","status","type","email"]
            )
            writer.writeheader()
            writer.writerows(updated_rows)

        time.sleep(10)

# =========================
# UI (ANTIGRAVITY MODERN)
# =========================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Scheduler</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: radial-gradient(circle at top, #0a0a0a, #000);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.glow {
    position: fixed;
    width: 400px;
    height: 400px;
    background: cyan;
    filter: blur(200px);
    opacity: 0.15;
    top: -100px;
    left: -100px;
    z-index: -1;
}

.container {
    width: 100%;
    max-width: 420px;
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(25px);
    box-shadow: 0 0 40px rgba(0,255,255,0.1);
    animation: float 5s ease-in-out infinite;
}

@keyframes float {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

h1 {
    text-align: center;
    margin-bottom: 20px;
    font-weight: 500;
    background: linear-gradient(90deg, cyan, lime);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

input, select {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: none;
    background: rgba(255,255,255,0.08);
    color: white;
    outline: none;
    transition: 0.25s;
}

input:focus, select:focus {
    transform: scale(1.03);
    box-shadow: 0 0 12px rgba(0,255,255,0.4);
}

button {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: none;
    margin-top: 12px;
    background: linear-gradient(90deg, cyan, lime);
    color: black;
    font-weight: bold;
    cursor: pointer;
    transition: 0.25s;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,255,200,0.5);
}

h3 {
    margin-top: 25px;
    opacity: 0.8;
}

.task {
    background: rgba(255,255,255,0.05);
    padding: 14px;
    margin-top: 12px;
    border-radius: 14px;
    position: relative;
    transition: 0.3s;
    animation: fadeIn 0.4s ease;
}

.task:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(0,255,255,0.1);
}

.delete {
    position: absolute;
    right: 10px;
    top: 10px;
    cursor: pointer;
    color: red;
}

.status {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 8px;
    margin-top: 6px;
    display: inline-block;
}

.pending { background: orange; color: black; }
.done { background: lime; color: black; }

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
</head>

<body>

<div class="glow"></div>

<div class="container">
    <h1>🚀 AI Scheduler</h1>

    <div class="form-group">
        <input id="topic" placeholder="Task">
        <input id="date" type="date">
        <input id="time" type="time">

        <select id="type">
            <option value="email draft">Email</option>
            <option value="reminder">Reminder</option>
        </select>

        <input id="email" placeholder="Email">
    </div>

    <button onclick="addTask()">Add Task</button>

    <h3>Tasks</h3>
    <div id="taskList"></div>
</div>

<script>
async function addTask() {
    const data = {
        topic: topic.value,
        date: date.value,
        time: time.value,
        type: type.value,
        email: email.value
    };

    await fetch("/add-task", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    topic.value = "";
    date.value = "";
    time.value = "";
    email.value = "";
    type.selectedIndex = 0;

    loadTasks();
}

async function loadTasks() {
    const res = await fetch("/tasks");
    const tasks = await res.json();

    const container = document.getElementById("taskList");
    container.innerHTML = "";

    tasks.forEach((t, i) => {
        container.innerHTML += `
        <div class="task">
            <span class="delete" onclick="deleteTask(${i})">❌</span>
            <b>${t.topic}</b><br>
            ${t.date} • ${t.time}<br>
            <span class="status ${t.status}">${t.status}</span>
        </div>
        `;
    });
}

async function deleteTask(index) {
    await fetch("/delete-task", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({index})
    });

    loadTasks();
}

loadTasks();
setInterval(loadTasks, 5000);
</script>

</body>
</html>
"""

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.json

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            data["topic"],
            data["date"],
            data["time"],
            "pending",
            data["type"],
            data["email"]
        ])

    return jsonify({"message": "Task added"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    with open(CSV_FILE, 'r') as f:
        return jsonify(list(csv.DictReader(f)))

@app.route("/delete-task", methods=["POST"])
def delete_task():
    index = int(request.json["index"])

    with open(CSV_FILE, 'r') as f:
        rows = list(csv.DictReader(f))

    if 0 <= index < len(rows):
        rows.pop(index)

    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["topic","date","time","status","type","email"]
        )
        writer.writeheader()
        writer.writerows(rows)

    return jsonify({"message": "Deleted"})

# =========================
# START
# =========================
if __name__ == "__main__":
    threading.Thread(target=task_scheduler, daemon=True).start()
    app.run(debug=False)
