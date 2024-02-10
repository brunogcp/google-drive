import argparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# Defina o escopo de acesso necessário
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def create_file(filename, mimetype, filepath):
    service = authenticate()
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")} - {filename} created.')

def list_files():
    service = authenticate()
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

def update_file(file_id, new_name, new_mimetype, new_filepath):
    service = authenticate()
    file_metadata = {'name': new_name}
    media = MediaFileUpload(new_filepath, mimetype=new_mimetype)
    updated_file = service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()
    print(f'File ID: {updated_file.get("id")} - {new_name} updated.')

def delete_file(file_id):
    service = authenticate()
    service.files().delete(fileId=file_id).execute()
    print(f'File {file_id} deleted.')

def main():
    parser = argparse.ArgumentParser(description="Google Drive API Python Script")
    parser.add_argument('action', help="Action to perform: create, list, update, delete")
    parser.add_argument('--filename', help="Name of the file to create/update")
    parser.add_argument('--mimetype', help="MIME type of the file to create/update")
    parser.add_argument('--filepath', help="Path of the file to create/update")
    parser.add_argument('--fileid', help="ID of the file to update/delete")
    parser.add_argument('--newname', help="New name of the file for update")
    args = parser.parse_args()

    if args.action == 'create':
        if args.filename and args.mimetype and args.filepath:
            create_file(args.filename, args.mimetype, args.filepath)
        else:
            print("Missing arguments for creation.")
    elif args.action == 'list':
        list_files()
    elif args.action == 'update':
        if args.fileid and args.newname and args.mimetype and args.filepath:
            update_file(args.fileid, args.newname, args.mimetype, args.filepath)
        else:
            print("Missing arguments for update.")
    elif args.action == 'delete':
        if args.fileid:
            delete_file(args.fileid)
        else:
            print("File ID required for deletion.")
    else:
        print("Invalid action. Please choose from 'create', 'list', 'update', 'delete'.")

if __name__ == '__main__':
    main()