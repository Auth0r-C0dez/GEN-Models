import os 
from dotenv import load_dotenv
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def reading_tasks(filepath):
    with open(filepath ,"r") as f:
        return f.read()
    
    
def summarise_task(tasks):
    prompt = f"""
You are a task priority planner assistant.

Your role is to help users organize their tasks based on urgency, importance, duration, and stakeholder sensitivity. Classify each task into one of the following categories:

- High Priority: Urgent and important. Must be done as soon as possible.
- Medium Priority: Important but not urgent. Should be scheduled or planned.
- Low Priority: Not urgent and less important. Can be delayed or delegated.

Consider these specific rules:
1. Tasks involving customers, managers, leadership, or anything that affects public reputation must be prioritized higher, even if they are not explicitly urgent.
2. Tasks that are estimated to take longer (e.g., writing reports, preparing presentations) and have stakeholder involvement should be scheduled **earlier** to allow enough time for completion.
3. Administrative or personal development tasks (e.g., inbox cleanup, internal learning) can be deprioritized unless otherwise stated.

Your output should include only a structured list under the following headers:
High Priority:
- task 1
- task 2

Medium Priority:
- task 3
- task 4

Low Priority:
- task 5
- task 6

Tasks to analyze:
{tasks}

Do not provide any explanations. Only return the sorted task list in the format above.
"""

  
    
    model = genai.GenerativeModel("gemini-1.5-flash")  # Free-tier model
    response = model.generate_content(prompt)
    return response.text




def setup_google_calendar():
    SCOPES = ['ENTER YOUR GOOGLE CALENDER API']
    creds = None

    # Check if token.json (saved credentials) already exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If not, go through login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the calendar API client
    service = build('calendar', 'v3', credentials=creds)
    return service

################################################



def schedule_tasks_on_calendar(tasks_by_priority, service):
    now = datetime.datetime.utcnow()
    day_offset = {'High': 0, 'Medium': 1, 'Low': 3}

    for priority, tasks in tasks_by_priority.items():
        offset = day_offset.get(priority, 5)

        for i, task in enumerate(tasks):
            # Calculate task date
            task_date = now + datetime.timedelta(days=offset + i)
            start_time = task_date.replace(hour=10, minute=0)
            end_time = task_date.replace(hour=11, minute=0)

            # Format ISO 8601 with timezone
            start = start_time.isoformat() + 'Z'
            end = end_time.isoformat() + 'Z'

            event = {
                'summary': task,
                'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
                'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'},
            }

            created_event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"✅ Scheduled: '{task}' at {created_event['start']['dateTime']}")
  


if __name__ == "__main__":
    # Step 1: Read tasks from file
    raw_tasks = reading_tasks("task.txt")
    
    # Step 2: Get Gemini summary
    summary = summarise_task(raw_tasks)
    print("\n Gemini Categorized Tasks:\n")
    print(summary)

    # Step 3: Parse Gemini output into dict
    def parse_tasks(summary):
        tasks_by_priority = {'High': [], 'Medium': [], 'Low': []}
        current = None
        for line in summary.splitlines():
            line = line.strip()
            if line.lower().startswith("high priority"):
                current = "High"
            elif line.lower().startswith("medium priority"):
                current = "Medium"
            elif line.lower().startswith("low priority"):
                current = "Low"
            elif line.startswith("-") and current:
                tasks_by_priority[current].append(line[2:].strip())
        return tasks_by_priority

    categorized_tasks = parse_tasks(summary)

    # Step 4: Authenticate Google Calendar
    service = setup_google_calendar()

    # Step 5: Schedule tasks
    print("\n📅 Scheduling tasks on Google Calendar...\n")
    schedule_tasks_on_calendar(categorized_tasks, service)
