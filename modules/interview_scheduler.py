import streamlit as st
from datetime import date, time
from modules.email_sender import EmailSender
from modules.calendar_scheduler import CalendarScheduler


class InterviewScheduler:

    def schedule(self, candidate=None):

        st.header("📅 Interview Scheduler")

        # Auto-fill candidate details
        candidate_name = st.text_input(
            "Candidate Name",
            value=candidate.get("candidate_name", "") if candidate else ""
        )

        candidate_email = st.text_input(
            "Candidate Email",
            value=candidate.get("email", "") if candidate else ""
        )

        interview_date = st.date_input(
            "Select Interview Date",
            min_value=date.today()
        )

        interview_time = st.time_input(
            "Select Interview Time",
            value=time(10, 0)
        )

        interview_mode = st.selectbox(
            "Interview Mode",
            ["Online", "Offline"]
        )

        interviewer = st.text_input(
            "Interviewer Name"
        )

        if st.button("Schedule Interview"):

            if not candidate_name.strip():
                st.error("Please enter Candidate Name")
                return

            if not candidate_email.strip():
                st.error("Please enter Candidate Email")
                return

            if not interviewer.strip():
                st.error("Please enter Interviewer Name")
                return

            sender = EmailSender()

            success = sender.send_interview_email(
                candidate_email=candidate_email.strip(),
                candidate_name=candidate_name.strip(),
                interview_date=interview_date,
                interview_time=interview_time,
                interview_mode=interview_mode,
                interviewer=interviewer.strip()
            )

            if success:

                calendar = CalendarScheduler()

                event_link = calendar.create_event(
                    candidate_name,
                    interview_date,
                    interview_time,
                    interviewer
                )

                st.success("✅ Interview Scheduled Successfully!")
                st.success("📧 Email Sent Successfully!")
                st.success("📅 Google Calendar Event Created!")

                if event_link:
                    st.markdown(f"[📅 Open Calendar Event]({event_link})")

                st.info(f"""
### 📋 Interview Details

📅 **Date:** {interview_date}

🕒 **Time:** {interview_time}

💻 **Mode:** {interview_mode}

👤 **Interviewer:** {interviewer}
""")

            else:
                st.error("❌ Failed to send interview email.")