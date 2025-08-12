# auth.py
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path

# Required permissions (read/write emails)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    # Check if token.json exists (already authenticated)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, log in via browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh expired token
        else:
            # Launch OAuth flow (opens browser)
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(host='localhost', port=8080, open_browser=False)
        
        # Save the token for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

# Test the function
if __name__ == '__main__':
    get_gmail_service()
    print("Authentication successful! token.json generated.")