📌 AI Task Planning Agent

This project is an AI-powered task planner that uses Google’s Gemini API to categorize tasks into High, Medium, and Low priority, and then schedules them directly into Google Calendar.

It reads tasks from a file (task.txt), classifies them based on urgency, duration, and stakeholder sensitivity, and then automatically creates reminders/events in your calendar.

📂 File Structure
.
├── .env                 # Stores API keys and environment variables  
├── agent.py             # (Optional) extra logic/experiments with the agent  
├── credentials.json     # Google Cloud OAuth credentials  
├── task_doer.py         # Main script for task planning & scheduling  
├── task.txt             # Input file with user’s task list  
├── token.json           # Generated after first Google login (stores user tokens)  

🚀 Features

Uses Gemini 1.5 Flash (free tier) for task classification.

Categorizes tasks based on:
✅ Urgency & deadlines
✅ Duration of tasks
✅ Customer/manager/public involvement

Adds tasks as calendar events in your Gmail account.

Automatically saves OAuth tokens for future runs.

Prevents repeated manual login by using token.json.

⚙️ Setup Instructions
1️⃣ Clone the Project
git clone https://github.com/Auth0r-CodezGEN-Models/Agents/Task-Scheduler.git
cd Task-Scheduler

2️⃣ Install Dependencies
pip install -r requirements.txt




3️⃣ Configure API Keys
🔹 Gemini API (AI Model)

Go to Google AI Studio
.

Generate a free Gemini API key.

Save it in .env file:

GEMINI_API_KEY=your_gemini_api_key_here

🔹 Google Calendar API

Go to Google Cloud Console
.

Create a New Project → Enable Google Calendar API.

Configure OAuth Consent Screen (External, add calendar.events scope).

Create OAuth Client ID → Select Desktop Application.

Download the JSON → Save as:

credentials.json

4️⃣ Authentication Flow

First run → Browser window opens → Sign in with Google → Allow Calendar Access.

A token.json file will be created and saved locally.

On future runs, your script will reuse this token.

📝 Usage
Step 1: Add Tasks

Write your tasks in task.txt, e.g.:

- Prepare client presentation (3 hours, deadline: Tuesday)
- Respond to customer complaints (2 hours, deadline: Today)
- Draft quarterly budget report (5 hours, deadline: Thursday)
- Team meeting notes (1 hour, deadline: Friday)
- Update website (4 hours, deadline: Sunday)

Step 2: Run the Script
python task_doer.py

Step 3: Output

🧠 Gemini categorizes tasks:

High Priority:
- Respond to customer complaints
- Draft quarterly budget report

Medium Priority:
- Prepare client presentation
- Team meeting notes

Low Priority:
- Update website


📅 Script schedules tasks in your Google Calendar:

✅ Scheduled: 'Respond to customer complaints' at 2025-09-19T10:00:00Z
✅ Scheduled: 'Draft quarterly budget report' at 2025-09-21T10:00:00Z

🔐 Token Management

credentials.json → Permanent client secret from Google Cloud.

token.json → Generated automatically after first login.

If token expires or breaks, delete token.json and rerun script to log in again.

📌 Future Enhancements (under development)

Auto-detect free time slots instead of fixed scheduling.

Integration with WhatsApp Business API (user sends tasks directly via WhatsApp).

Task removal (cancel events from Calendar on user request).

Multi-user SaaS deployment with subscriptions.
