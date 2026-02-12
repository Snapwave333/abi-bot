import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarManager:
    def __init__(self):
        self.logger = logging.getLogger("ABI_Bot.GCal")
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticates with Google API."""
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    self.logger.info("Refreshing expired token...")
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.error(f"Token refresh failed: {e}")
                    creds = None # Force re-login

            if not creds:
                if not os.path.exists('credentials.json'):
                    self.logger.critical("'credentials.json' not found.")
                    return
                
                self.logger.info("Initiating login flow...")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)
        self.logger.info("Google Service Authenticated")

    def sync_event(self, event_data, unique_id):
        """Syncs a single event. Returns status string."""
        if not self.service:
            return "NO_SERVICE"

        event_body = {
            'summary': event_data['summary'],
            'location': event_data['location'],
            'description': event_data['description'],
            'start': {
                'dateTime': event_data['start'].isoformat(),
                'timeZone': 'America/Denver',
            },
            'end': {
                'dateTime': event_data['end'].isoformat(),
                'timeZone': 'America/Denver',
            },
            'id': unique_id,
            'colorId': '6',
            'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 24 * 60}]},
        }

        try:
            self.service.events().insert(calendarId='primary', body=event_body).execute()
            self.logger.info(f"Added event: {event_data['summary']}")
            return "ADDED"
        except Exception as e:
            if "already exists" in str(e) or "409" in str(e):
                # Optional details update could go here
                return "SKIPPED"
            self.logger.error(f"Failed to add event {event_data['summary']}: {e}")
            return f"ERROR: {e}"
