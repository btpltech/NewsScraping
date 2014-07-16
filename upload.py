import httplib2
import pprint
import os
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

def upload_data():
	CLIENT_ID = 'Enter Client ID'
	CLIENT_SECRET = "Enter Client Secret"
	OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
	REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

	flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
	authorize_url = flow.step1_get_authorize_url()
	print 'Go to the following link in your browser: ' + authorize_url
	code = raw_input('Enter verification code: ').strip()
	credentials = flow.step2_exchange(code)

	http = httplib2.Http()
	http = credentials.authorize(http)

	drive_service = build('drive', 'v2', http=http)

	for file in os.listdir('./'):
		if file.endswith(".txt") or file.endswith(".csv"):
			FILENAME = file
			media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
			body = {
					'title': FILENAME,
					'description': 'A test document',
					'mimeType': 'text/plain'
					}

			file = drive_service.files().insert(body=body, media_body=media_body).execute()
			pprint.pprint(file)
upload_data()
