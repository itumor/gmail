import google.auth
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
import requests

# Get your credentials from https://console.cloud.google.com/apis/credentials
creds = Credentials.from_authorized_user_file("credentials.json")

# Set up the API endpoint
api_endpoint = "https://photoslibrary.googleapis.com/v1/mediaItems"

# Set up the session with the credentials
session = AuthorizedSession(creds)

# Set up the request headers
headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer " + creds.token,
}

# Set up the request parameters
params = {
    "pageSize": 100,
}

# Send the initial request to get the first page of results
response = session.get(api_endpoint, headers=headers, params=params).json()

# Keep looping until all pages have been downloaded
while "nextPageToken" in response:
    # Get the next page token
    next_page_token = response["nextPageToken"]
    
    # Add the next page token to the request parameters
    params["pageToken"] = next_page_token
    
    # Send the request to get the next page of results
    response = session.get(api_endpoint, headers=headers, params=params).json()
    
    # Loop through the media items in the response and download them
    for item in response["mediaItems"]:
        # Get the photo URL
        photo_url = item["baseUrl"] + "=d"

        # Download the photo
        r = requests.get(photo_url)
        
        # Save the photo to disk
        with open(item["filename"], "wb") as f:
            f.write(r.content)