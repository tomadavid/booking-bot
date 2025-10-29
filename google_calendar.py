import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

"""
    Functions that interact directly with the Google Calendar API (lowest level)

    -> Raw interaction with event scheduling
"""

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"]


"""
    Get hosts credentials (token_host.json)
    Used in testing phase -> In production the file is already in the environment
"""
def get_host_credentials():
  creds = None

  if os.path.exists("token_host.json"):
    creds = Credentials.from_authorized_user_file("token_host.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES[0]
      )
      creds = flow.run_local_server(port=0)

    with open("token_host.json", "w") as token:
      token.write(creds.to_json())
  return creds


"""
    Get client credentials (token_client.json)
    Keep in production so new clients can log with Google OAuth
"""
def get_client_credentials():
  creds = None

  if os.path.exists("token_client.json"):
    creds = Credentials.from_authorized_user_file("token_client.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)

    with open("token_client.json", "w") as token:
      token.write(creds.to_json())
  return creds


"""
    Add an event to host's and client's calendar

    -> Events is a tuple containing:
        (host's event, client's event)
"""
def add_calendar_event(host_creds, client_creds, events):
  try:
    #add on host
    service_host = build("calendar", "v3", credentials=host_creds)
    event = service_host.events().insert(calendarId='primary', body=events[0]).execute()
    print("Event created successfully on host:", event.get('htmlLink'))   

    #add on client
    service_client = build("calendar", "v3", credentials=client_creds)
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    event = service_client.events().insert(calendarId='primary', body=events[1]).execute()
    print("Event created successfully on client:", event.get('htmlLink'))
    return event.get('htmlLink')

  except HttpError as error:
    print(f"An error occurred: {error}")


"""
    Creates an event

    -> Returns two events is a tuple containing:
        (host's event, client's event)
"""
def create_event(start_time: datetime.datetime, client_email):
  events = [
    # host's event        
    {
    'summary': 'Booking',
    'location': 'Online',
    'description': 'Your online booking',
    'start': {
        'dateTime': start_time.isoformat(),
        'timeZone': 'Europe/Lisbon'
    },
    'end': {
        'dateTime': (start_time + datetime.timedelta(hours=1)).isoformat(),
        'timeZone': 'Europe/Lisbon'
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
    ],
    'attendees': [
        {'email': client_email} #client's email
    ]
  }, 

  # client's event
  {
    'summary': 'Booking',
    'location': 'Online',
    'description': 'Your online booking',
    'start': {
        'dateTime': start_time.isoformat(),
        'timeZone': 'Europe/Lisbon'
    },
    'end': {
        'dateTime': (start_time + datetime.timedelta(hours=1)).isoformat(),
        'timeZone': 'Europe/Lisbon'
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
    ],
    'attendees': [
        {'email': 'vidamot24@gmail.com'} #host's email
    ]
  }]
  return events


"""
    Returns the client's email so the host can add it to their event
    -> Make user know who scheduled the event
"""
def get_client_email(client_creds):
  service = build('people', 'v1', credentials=client_creds)
  client_profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
  return client_profile['emailAddresses'][0]['value']

