import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_cred():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("./config/gdtoken.json"):
        creds = Credentials.from_authorized_user_file("./config/gdtoken.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./config/gdcr.json", SCOPES
            )
            creds = flow.run_local_server(port=9000)
        # Save the credentials for the next run
        with open("./config/gdtoken.json", "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)