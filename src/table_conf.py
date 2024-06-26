import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheet():
    credentials = None
    if (os.path.exists("./config/Lasttoken.json")):
        credentials = Credentials.from_authorized_user_file("./config/Lasttoken.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("./config/lastCred.json", SCOPES)
            credentials = flow.run_local_server(port=9000)

        with open("./config/Lasttoken.json", "w") as token:
            token.write(credentials.to_json())

    return build("sheets", "v4", credentials=credentials)
