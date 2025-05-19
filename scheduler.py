import schedule
import time
import requests
from datetime import datetime

def check_reminders():
    reminders = requests.get("http://localhost:8000/get-reminders").json()
    now = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%a")
    
    for reminder in reminders["reminders"]:
        if now == reminder["time"][:5] and today in reminder["days"]:
            print(f"ALERT: Take {reminder['dosage']} of {reminder['medication']}")

# Run every minute
schedule.every(1).minutes.do(check_reminders)

while True:
    schedule.run_pending()
    time.sleep(1)