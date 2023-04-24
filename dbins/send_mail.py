import os
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from requests import HTTPError
from django.conf import settings

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists(settings.GOOGLE_TOKEN):
    creds = Credentials.from_authorized_user_file(settings.GOOGLE_TOKEN, SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_KEY, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(settings.GOOGLE_TOKEN, 'w') as token:
        token.write(creds.to_json())

def send_mail(to: str, subject: str, body: str):
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        return F'sent message to {message} Message Id: {message["id"]}'
    except HTTPError as error:
        return F'An error occurred: {error}'
    
send_mail('bekjan02003@gmail.com', 'test', 'test')
