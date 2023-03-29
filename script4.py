import os.path
from concurrent import futures

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://mail.google.com/']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        
    # Get a list of all emails in the "Social" category
    next_page_token = None
    
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            # Get the next batch of messages
            request = service.users().messages().list(
                userId="me",
                q='in:spam',
                pageToken=next_page_token
            )
            response = request.execute()
            messages = response.get('messages', [])

            # Process the messages in the current batch
            futures_to_messages = {}
            for message in messages:
                # Submit each message to be processed asynchronously
                futures_to_messages[executor.submit(process_message, service, message)] = message
            
            # Wait for all processing to complete
            for future in futures.as_completed(futures_to_messages):
                message = futures_to_messages[future]
                try:
                    future.result()
                except HttpError as error:
                    print(f'An error occurred while processing message {message["id"]}: {error}')
            
            # Check if there are more messages to retrieve
            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
            else:
                break


def process_message(service, message):
    """Processes a single message, e.g. deletes it."""
    service.users().messages().delete(userId="me", id=message['id']).execute()
    

if __name__ == '__main__':
    main()
