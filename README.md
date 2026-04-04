AI Task Scheduler

An intelligent, automated task scheduling system that combines AI-generated content, email automation, and a modern interactive dashboard to streamline daily workflows.

✨ Overview

AI Task Scheduler is a lightweight yet powerful web application that allows users to:

Schedule tasks with precise date and time
Automatically generate AI-powered content
Send emails or reminders without manual intervention
Track task status in real time (Pending / Completed)
Manage tasks through a clean, modern UI

This project demonstrates the integration of automation + AI + frontend UX into a single cohesive system.

⚙️ Features
🧠 AI-Powered Content Generation
Uses Sarvam AI API to generate:
Professional email drafts
Smart reminders
⏰ Automated Task Execution
Background scheduler continuously monitors tasks
Executes tasks when conditions are met
📧 Email Automation
Sends emails via Gmail SMTP
Supports:
AI-generated email drafts
Reminder notifications
📋 Task Management Dashboard
View all tasks in real time
Status indicators:
🟡 Pending
🟢 Done
Delete tasks instantly
🎨 Modern UI (Antigravity Design)
Glassmorphism interface
Smooth animations and transitions
Fully responsive layout
Clean and minimal UX
🏗️ Tech Stack

Backend

Python
Flask
Threading (for scheduler)

Frontend

HTML + CSS + Vanilla JavaScript
Glassmorphism + animated UI

APIs & Services

Sarvam AI API (text generation)
Gmail SMTP (email delivery)

Storage

CSV (lightweight local database)
🔐 Security

Sensitive credentials are securely handled using environment variables.

Required Environment Variables
setx EMAIL_USER "your_email@gmail.com"
setx EMAIL_PASS "your_app_password"
setx SARVAM_API_KEY "your_api_key"

⚠️ Restart your terminal after running the above commands.

🚀 Getting Started
1. Clone the Repository
git clone <your-repo-url>
cd <your-project-folder>
2. Install Dependencies
pip install flask flask-cors requests
3. Set Environment Variables

Use the setx commands mentioned above.

4. Run the Application
python app.py
5. Open in Browser
http://127.0.0.1:5000
🧠 How It Works
User creates a task via the UI
Task is stored in a CSV file
Background scheduler checks tasks every 10 seconds
When time matches:
AI generates content (if needed)
Email is sent automatically
Task status updates to done
📸 Key Highlights
Real-time task updates without page reload
Smooth animated UI interactions
Fully automated workflow system
Clean separation of backend and frontend logic
📈 Future Improvements
🔐 User authentication system
🗄️ Database integration (MongoDB / PostgreSQL)
📊 Task filtering (Pending / Done views)
✏️ Edit task functionality
☁️ Cloud deployment (Render / AWS / Vercel)
📱 Mobile app version
PPT: https://gamma.app/docs/AI-Scheduler-47i9iu7q3tl4d0p
