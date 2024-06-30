from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
import os
from googleapiclient.errors import HttpError
import json

load_dotenv()
scope = ['https://www.googleapis.com/auth/drive']
service_account_info = {
  "type": "service-account",
  "project_id": os.environ['GOOGLE_PROJECT_ID'],
  "private_key_id": os.environ['GOOGLE_PRIVATE_KEY_ID'],
  "private_key": os.environ['GOOGLE_PRIVATE_KEY'],
  "client_email": os.environ['GOOGLE_CLIENT_EMAIL'],
  "client_id": os.environ['GOOGLE_CLIENT_ID'],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ['GOOGLE_CLIENT_X509_CERT_URL'],
  "universe_domain": "googleapis.com"
}
credentials = service_account.Credentials.from_service_account_info(
                              info=service_account_info, 
                              scopes=scope)
service = build('drive', 'v3', credentials=credentials)

def download_pdf(fileId):
    try:
        file_metadata = service.files().get(fileId=fileId).execute()
        fileName = file_metadata["name"]
        request_file = service.files().get_media(fileId=fileId)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request_file)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f'Download {int(status.progress() * 100)}.')

        file_retrieved = file.getvalue()
        with open(f"docs/{fileName}", "wb") as f:
            f.write(file_retrieved)

    except HttpError as error:
        print(f'An error occurred: {error}')
