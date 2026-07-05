import os
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailReader:

    def __init__(self):

        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build(
            "gmail",
            "v1",
            credentials=creds
        )

    def get_latest_resume_email(self):

        print("Searching Gmail for PDF attachments...")

        results = self.service.users().messages().list(
            userId="me",
            q="has:attachment filename:pdf",
            maxResults=5
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            print("No PDF emails found.")
            return None

        print(f"Found {len(messages)} email(s).")

        os.makedirs("data/resumes", exist_ok=True)

        for message in messages:

            msg = self.service.users().messages().get(
                userId="me",
                id=message["id"]
            ).execute()

            payload = msg.get("payload", {})

            parts = payload.get("parts", [])

            if not parts:
                parts = [payload]

            for part in parts:

                filename = part.get("filename", "")

                if filename.lower().endswith(".pdf"):

                    print("Downloading:", filename)

                    attachment_id = part.get(
                        "body",
                        {}
                    ).get("attachmentId")

                    if not attachment_id:
                        continue

                    attachment = (
                        self.service.users()
                        .messages()
                        .attachments()
                        .get(
                            userId="me",
                            messageId=message["id"],
                            id=attachment_id
                        )
                        .execute()
                    )

                    file_data = base64.urlsafe_b64decode(
                        attachment["data"]
                    )

                    filepath = os.path.join(
                        "data",
                        "resumes",
                        filename
                    )

                    with open(filepath, "wb") as f:
                        f.write(file_data)

                    print("Saved to:", filepath)

                    return filepath

        print("No PDF attachment found.")

        return None


if __name__ == "__main__":

    reader = GmailReader()

    path = reader.get_latest_resume_email()

    print("\nDownloaded File:")
    print(path)