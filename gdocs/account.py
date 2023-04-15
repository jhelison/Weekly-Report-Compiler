import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from gdocs.scopes import SCOPES


# Authenticate on google
def authenticate_google():
    # Define the credentials files
    token_file = os.getenv("GOOGLE_TOKEN")
    credential_file = os.getenv("GOOGLE_CRED_FILE")

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("docs", "v1", credentials=creds)


# Get a document content based on the document ID
def get_document_content(document_id: str) -> dict:
    service = authenticate_google()

    # Get the document content
    result = (
        service.documents().get(documentId=document_id, fields="body/content").execute()
    )
    return result.get("body", {}).get("content", [])


# Apply requests to a document
def apply_content(document_id: str, requests: list):
    service = authenticate_google()

    service.documents().batchUpdate(
        documentId=document_id, body={"requests": requests}
    ).execute()
