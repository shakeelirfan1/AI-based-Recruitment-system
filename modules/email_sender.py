import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


class EmailSender:

    def __init__(self):
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_APP_PASSWORD")

    def send_interview_email(
        self,
        candidate_email,
        candidate_name,
        interview_date,
        interview_time,
        interview_mode,
        interviewer
    ):

        subject = "Interview Invitation | AI Recruitment System"

        body = f"""
Dear {candidate_name},

Congratulations!

We are pleased to inform you that you have been shortlisted for the next stage of our recruitment process.

Interview Details
-------------------------
Date: {interview_date}
Time: {interview_time}
Mode: {interview_mode}
Interviewer: {interviewer}

If your interview is online, the meeting link will be shared before the interview.

Please reply to this email if you have any questions.

Best Regards,
HR Team
AI Recruitment System
"""

        message = MIMEMultipart()

        message["From"] = self.email
        message["To"] = candidate_email.strip()
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        try:

            print("=" * 50)
            print("FROM :", self.email)
            print("TO   :", candidate_email)
            print("SUBJECT :", subject)
            print("=" * 50)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(
                self.email,
                self.password
            )

            server.sendmail(
                self.email,
                [candidate_email.strip()],
                message.as_string()
            )

            server.quit()

            print("Email Sent Successfully")

            return True

        except Exception as e:

            print("EMAIL ERROR")
            print(type(e))
            print(e)

            return False


if __name__ == "__main__":

    sender = EmailSender()

    sender.send_interview_email(
        candidate_email="YOUR_TEST_EMAIL@gmail.com",
        candidate_name="Shakeel",
        interview_date="10 July 2026",
        interview_time="10:00 AM",
        interview_mode="Online",
        interviewer="HR Team"
    )