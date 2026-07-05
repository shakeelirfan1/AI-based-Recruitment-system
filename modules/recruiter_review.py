import streamlit as st


class RecruiterReview:

    def show(self, candidate):

        st.header("👨‍💼 Recruiter Manual Review")

        name = st.text_input(
            "Candidate Name",
            candidate.get("name", "")
        )

        email = st.text_input(
            "Email",
            candidate.get("email", "")
        )

        phone = st.text_input(
            "Phone",
            candidate.get("phone", "")
        )

        skills = st.text_area(
            "Skills",
            candidate.get("skills", "")
        )

        experience = st.text_area(
            "Experience",
            candidate.get("experience", "")
        )

        recommendation = st.selectbox(
            "Recommendation",
            [
                "Shortlist",
                "Review",
                "Reject"
            ]
        )

        status = st.selectbox(
            "Application Status",
            [
                "New",
                "Review",
                "Interview Scheduled",
                "Rejected",
                "Selected"
            ]
        )

        notes = st.text_area(
            "Recruiter Notes"
        )

        if st.button("💾 Save Changes"):

            candidate["name"] = name
            candidate["email"] = email
            candidate["phone"] = phone
            candidate["skills"] = skills
            candidate["experience"] = experience
            candidate["recommendation"] = recommendation
            candidate["status"] = status
            candidate["notes"] = notes

            st.success("Candidate Updated Successfully!")

            return candidate

        return None