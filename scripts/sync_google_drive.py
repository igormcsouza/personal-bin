import os
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Define the ID of the folder you want to upload
folder_id = '13-vlXGMJV9hBLC5ENP2uv43v8lovNUag'

# Define the credentials you need to perform the upload
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive'])
elif os.path.exists('creds.json'):
    creds = service_account.Credentials.from_service_account_file('creds.json', scopes=['https://www.googleapis.com/auth/drive'])
else:
    print('Please provide authentication credentials.')

# Define the function that will upload the folder
def upload_folder(folder_path):
    service = build('drive', 'v3', credentials=creds)
    folder_metadata = {'name': os.path.basename(folder_path), 'parents': [folder_id], 'mimeType': 'application/vnd.google-apps.folder'}
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_metadata = {'name': os.path.join(os.path.relpath(root, folder_path), filename), 'parents': [folder['id']]}
            media = {'media_body': os.path.join(root, filename)}
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# Define the function that will check for changes in the folder and upload it if necessary
def check_for_changes(folder_path):
    last_modification_time = 0
    while True:
        modification_time = os.path.getmtime(folder_path)
        if modification_time > last_modification_time:
            print('Folder has been modified. Uploading...')
            upload_folder(folder_path)
            last_modification_time = modification_time
        time.sleep(60)

# Start checking for changes in the folder
check_for_changes('/home/universe.dart.spb/isouza/Documents/personal-docs')

