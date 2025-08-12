# auto_responder.py (updated)
import json
from auth import get_gmail_service
from googleapiclient.discovery import build
import base64

def load_config():
    with open('config.json') as f:
        return json.load(f)

def create_reply(sender, subject, template):
    return f"From: me\nTo: {sender}\nSubject: Re: {subject}\n\n{template}"

def send_reply(service, original_msg_id, reply_text, mark_as_read):
    raw_reply = base64.urlsafe_b64encode(reply_text.encode('utf-8')).decode('utf-8')
    service.users().messages().send(userId='me', body={'raw': raw_reply}).execute()
    if mark_as_read:
        service.users().messages().modify(
            userId='me',
            id=original_msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

def process_emails():
    config = load_config()
    service = build('gmail', 'v1', credentials=get_gmail_service())
    messages = service.users().messages().list(
        userId='me',
        labelIds=['INBOX', 'UNREAD']
    ).execute().get('messages', [])

    for msg in messages:
        email = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['Subject', 'From']
        ).execute()
        headers = email['payload']['headers']
        subject = next(h['value'] for h in headers if h['name'] == 'Subject')
        sender = next(h['value'] for h in headers if h['name'] == 'From')

        for rule in config['rules']:
            field_value = subject if rule['condition']['field'] == 'subject' else sender
            if rule['condition']['contains'].lower() in field_value.lower():
                print(f"Applying rule '{rule['name']}' to email: {subject}")
                reply_text = create_reply(sender, subject, rule['action']['reply_template'])
                send_reply(service, msg['id'], reply_text, rule['action']['mark_as_read'])

if __name__ == '__main__':
    process_emails()