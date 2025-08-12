import csv
import base64
import json
from googleapiclient.discovery import build
from logger import log_action
from auth import get_gmail_service

def load_config():
    with open('config.json') as f:
        return json.load(f)

def create_reply(sender, subject, template):
    return f"From: me\nTo: {sender}\nSubject: Re: {subject}\n\n{template}"

def send_reply(service, original_msg_id, reply_text, mark_as_read):
    raw_reply = base64.urlsafe_b64encode(reply_text.encode('utf-8')).decode('utf-8')
    service.users().messages().send(
        userId='me',
        body={'raw': raw_reply}
    ).execute()
    if mark_as_read:
        service.users().messages().modify(
            userId='me',
            id=original_msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

def process_emails():
    print("Starting email processing...")
    
    # Initialize log file with header
    try:
        with open('email_logs.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Subject", "From", "Rule", "Action"])
        print("Initialized log file")
    except Exception as e:
        print(f"Failed to initialize log file: {e}")
        return

    try:
        config = load_config()
        creds = get_gmail_service()
        service = build('gmail', 'v1', credentials=creds)
        print("Authenticated with Gmail API")
        
        messages = service.users().messages().list(
            userId='me',
            labelIds=['INBOX', 'UNREAD']
        ).execute().get('messages', [])
        
        print(f"Found {len(messages)} unread messages")
        
        for msg in messages:
            print(f"\nProcessing message ID: {msg['id']}")
            
            email = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['Subject', 'From']
            ).execute()
            
            headers = email['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            
            print(f"Processing email: {subject[:30]}... from {sender}")
            
            email_data = {'subject': subject, 'from': sender}

            for rule in config['rules']:
                field = rule['condition']['field']
                keyword = rule['condition']['contains'].lower()
                
                print(f"Checking rule: {rule['name']} (looking for '{keyword}' in {field})")
                
                if keyword in email_data[field].lower():
                    print("Rule matched! Taking action...")
                    log_action(email_data, rule['name'], "Replied")
                    reply_text = create_reply(sender, subject, rule['action']['reply_template'])
                    send_reply(service, msg['id'], reply_text, rule['action']['mark_as_read'])
                    print("Reply sent and logged")
    
    except Exception as e:
        print(f"Error processing emails: {e}")
        raise

if __name__ == '__main__':
    process_emails()