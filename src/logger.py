import csv
from datetime import datetime
import os

def log_action(email, rule_name, action_taken):
    try:
        file_exists = os.path.isfile('email_logs.csv')
        
        with open('email_logs.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Subject", "From", "Rule", "Action"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                email['subject'],
                email['from'],
                rule_name,
                action_taken
            ])
        print(f"Successfully logged action for {email['subject']}")
    except Exception as e:
        print(f"Failed to log action: {e}")
        raise