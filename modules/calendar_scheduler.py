from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os
import pickle
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalendarScheduler:

    def __init__(self):

        creds = None

        if os.path.exists("calendar_token.pkl"):
            with open("calendar_token.pkl", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open("calendar_token.pkl", "wb") as token:
                pickle.dump(creds, token)

        self.service = build("calendar", "v3", credentials=creds)

    def create_event(
        self,
        candidate_name,
        interview_date,
        interview_time,
        interviewer
    ):

        start = datetime.combine(
            interview_date,
            interview_time
        )

        end = start.replace(hour=start.hour + 1)

        event = {
            "summary": f"Interview - {candidate_name}",

            "description": f"Interviewer: {interviewer}",

            "start": {
                "dateTime": start.isoformat(),
                "timeZone": "Asia/Kolkata",
            },

            "end": {
                "dateTime": end.isoformat(),
                "timeZone": "Asia/Kolkata",
            }
        }

        event = self.service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        print("=" * 50)
        print("Event Created Successfully")
        print("Calendar ID :", event.get("organizer", {}).get("email"))
        print("Event ID    :", event.get("id"))
        print("HTML Link   :", event.get("htmlLink"))
        print("Start       :", event.get("start"))
        print("=" * 50)

        return event.get("htmlLink")