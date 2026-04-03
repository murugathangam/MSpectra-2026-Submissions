🚀 AI Task Scheduler

A modern, AI-powered task scheduling web app that automatically generates emails or reminders and sends them at the scheduled time.

✨ Features
📅 Schedule tasks with date & time
🧠 AI-generated:
Email drafts
Smart reminders
📧 Automatic email sending via Gmail SMTP
⚡ Real-time task updates (auto-refresh UI)
🗂️ CSV-based lightweight database
🎨 Modern glassmorphism UI
🛠️ Tech Stack
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript (embedded)
AI Model: LLaMA 3 via Ollama
Storage: CSV file
Email Service: Gmail SMTP
📁 Project Structure
project/
│── app.py
│── tasks.csv
⚙️ Setup Instructions
1. Install Dependencies
pip install flask flask-cors requests
2. Install & Run Ollama (for AI)

Download Ollama and run:

ollama run llama3

Make sure it's running at:

http://localhost:11434
3. Set Email Password (IMPORTANT)

Set your Gmail App Password as an environment variable:

Windows (PowerShell):
setx EMAIL_PASS "your_app_password"
Mac/Linux:
export EMAIL_PASS="your_app_password"
4. Run the App
python app.py

Open in browser:

http://localhost:5000
📌 How It Works
Add a task (topic, date, time, type, email)
Task is stored in tasks.csv
Background thread checks tasks every 10 seconds
When time matches:
AI generates content using LLaMA 3
Email is sent automatically
Task marked as ✅ done
🔄 Task Types
Type	Action
Email Draft	Sends AI-generated professional email
Reminder	Sends short reminder message
🧠 AI Integration

Uses local LLM via Ollama:

Email Prompt → "Write a professional email about {topic}"
Reminder Prompt → "Write a short reminder about {topic}"
⚠️ Important Notes
Use Gmail App Password, NOT your real password
Ensure Ollama is running before starting the app
Email sending may fail if:
App password is missing
Internet is down
SMTP blocked
🚀 Future Improvements
Google Calendar integration
Push notifications (instead of email)
User authentication
Database (SQLite / MongoDB)
Task priority & categories
Mobile app version