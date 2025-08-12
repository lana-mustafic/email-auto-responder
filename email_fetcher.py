# email_fetcher.py
from auth import get_gmail_service
from googleapiclient.discovery import build

def fetch_unread_emails():
    # Authenticate and create Gmail service
    creds = get_gmail_service()
    service = build('gmail', 'v1', credentials=creds)
    
    # Fetch unread emails from inbox
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX', 'UNREAD']
    ).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No unread emails found.")
    else:
        print(f"Found {len(messages)} unread emails:")
        for msg in messages:
            # Get email details (subject, sender)
            email = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['Subject', 'From']
            ).execute()
            
            # Extract headers
            headers = email['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            
            print(f"- Subject: {subject} | From: {sender}")

if __name__ == '__main__':
    fetch_unread_emails()