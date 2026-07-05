import streamlit as st
import pandas as pd
from pyairtable import Table
from dotenv import load_dotenv
import os

load_dotenv()


class RecruiterDashboard:

    def __init__(self):

        self.table = Table(
            os.getenv("AIRTABLE_TOKEN"),
            os.getenv("AIRTABLE_BASE_ID"),
            os.getenv("AIRTABLE_TABLE_NAME")
        )

    def show(self):

        st.title("📊 Recruiter Dashboard")

        records = self.table.all()

        if not records:
            st.warning("No candidates found.")
            return

        candidates = []

        for record in records:

            fields = record["fields"]

            candidates.append({
                "Candidate Name": fields.get("Name", ""),
                "Email": fields.get("Email", ""),
                "Experience": fields.get("Experience", ""),
                "Match Score": fields.get("Match Score", 0),
                "Application Status": fields.get("Application Status", ""),
                "Recommendation": fields.get("Recommendation", "")
            })

        df = pd.DataFrame(candidates)

        st.subheader("All Candidates")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.metric(
            "Total Candidates",
            len(df)
        )

        shortlisted = len(
            df[df["Application Status"] == "Shortlisted"]
        )

        review = len(
            df[df["Application Status"] == "Manual Review"]
        )

        rejected = len(
            df[df["Application Status"] == "Rejected"]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("✅ Shortlisted", shortlisted)
        col2.metric("🟡 Review", review)
        col3.metric("❌ Rejected", rejected)

        st.bar_chart(
            df["Application Status"].value_counts()
        )