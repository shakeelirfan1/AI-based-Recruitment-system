import streamlit as st


class Dashboard:

    def show(self, match_json):

        st.header("📊 Recruiter Dashboard")

        # Get match score
        score = float(
            str(match_json.get("match_score", 0))
            .replace("%", "")
            .strip()
        )

        # Convert 0.8 -> 80
        if score <= 1:
            score *= 100

        score = int(score)

        # Candidate Status
        shortlisted = 1 if score >= 80 else 0
        review = 1 if 60 <= score < 80 else 0
        rejected = 1 if score < 60 else 0

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Candidates", 1)
        col2.metric("Shortlisted", shortlisted)
        col3.metric("Need Review", review)
        col4.metric("Rejected", rejected)

        # Match Score
        st.subheader(f"🎯 Match Score: {score}%")
        st.progress(score / 100)

        # Candidate Status
        if score >= 80:
            st.success("✅ Candidate Shortlisted")
        elif score >= 60:
            st.warning("⚠️ Candidate Needs Review")
        else:
            st.error("❌ Candidate Rejected")

        # Dashboard Chart
        chart_data = {
            "Status": ["Shortlisted", "Review", "Rejected"],
            "Count": [shortlisted, review, rejected]
        }

        st.bar_chart(
            data={
                "Count": [shortlisted, review, rejected]
            }
        )