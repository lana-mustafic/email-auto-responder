# auto_responder.py
from auth import get_gmail_service
from googleapiclient.discovery import build
import base64

def create_reply(sender, subject):
    """Generate reply text (customize this!)"""
    return f"""From: me\nTo: {sender}\nSubject: Re: {subject}\n\n
    Thank you for your email! I'm currently unavailable but will respond soon.
    (This is an automated reply)"""

def send_reply(service, original_msg_id, reply_text):
    """Send the reply and mark original as read"""
    # Encode the reply
    raw_reply = base64.urlsafe_b64encode(reply_text.encode('utf-8')).decode('utf-8')
    
    # Send reply
    service.users().messages().send(
        userId='me',
        body={'raw': raw_reply}
    ).execute()
    
    # Mark original as read
    service.users().messages().modify(
        userId='me',
        id=original_msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

def process_emails():
    service = build('gmail', 'v1', credentials=get_gmail_service())
    
    # Fetch unread emails (reusing our fetcher logic)
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX', 'UNREAD']
    ).execute()
    messages = results.get('messages', [])

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
        
        # Rule: Reply if "urgent" is in subject
        if 'urgent' in subject.lower():
            print(f"Replying to: {subject}")
            reply_text = create_reply(sender, subject)
            send_reply(service, msg['id'], reply_text)

if __name__ == '__main__':
    process_emails()
    print("Auto-responder completed!")