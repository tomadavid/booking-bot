from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from parser import Output
from google_calendar import *

"""
    High level utility functions for event management (scheduling/canceling)
"""

def schedule_event(request : Output):
    # get credentials
    host_creds = get_host_credentials()
    client_creds = get_client_credentials()

    #get client email
    client_email = get_client_email(client_creds)

    #check event constraints
    invalid_event = check_if_time_interval_is_valid(request.schedule_datetime, request.duration)
    if invalid_event:
        return invalid_event
    if not check_if_slot_is_free(host_creds, request.schedule_datetime, request.schedule_datetime + request.duration):
        return f"The slot you are trying to book is already booked. Try a different one"
    
    # create events (one for host, other for client)
    events = create_event(request.schedule_datetime, client_email)

    # add event to calendar
    link = add_calendar_event(host_creds, client_creds, events)

    return f"Your booking for {str(request.schedule_datetime)} was sucessfuly confirmed!\n{link}"


# check constraints

""" 
    Checks if slot is available on host's calendar
"""

def check_if_slot_is_free(host_creds, start_time : datetime, end_time : datetime):
  
  start_time = start_time.replace(tzinfo=timezone.utc)
  end_time = end_time.replace(tzinfo=timezone.utc)
  service = build("calendar", "v3", credentials=host_creds)
  events_found = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_time.isoformat(),
            timeMax=end_time.isoformat(),
            maxResults=1,
            singleEvents=True,
        )
        .execute()
    )
  
  events = events_found.get("items", [])

  if events:
    return False
  
  return True


""" 
    Checks if specified time interval for booking is valid
    - interval -> Daily interval for bookings (ex: 9AM-6PM)
"""

def check_if_time_interval_is_valid(start_time, duration, interval=(9,18)):
    if datetime.now() > start_time:
        return "Bookings must be done to the future!"
    if datetime.now() + timedelta(minutes=30) > start_time:
        return "Bookings and cancelations must be done at least 30 minutes before its start time!"
    if datetime.now() + timedelta(days=7) < start_time:
        return "Bookings can be done at maximum one week before!"
    if start_time.minute != 0:
        return "Bookings must be done every hour!"
    if duration > timedelta(hours=2):
        return "Bookings cannot exceed 2 hours!"
    if duration < timedelta(minutes=30):
        return "Bookings cannot be less than 30 minutes!"
    if timedelta(hours=interval[0]) > timedelta(hours=start_time.hour) or timedelta(hours=interval[1]) < timedelta(hours=start_time.hour) or \
        timedelta(hours=interval[0]) > timedelta(hours=start_time.hour) + duration or timedelta(hours=interval[1]) < timedelta(hours=start_time.hour) + duration:
        return "Bookings must be between 9AM-6PM!"