import streamlit as st

from modules.resume_parser import ResumeParser
from modules.ai_extractor import AIExtractor
from modules.json_parser import JSONParser
from modules.jd_matcher import JDMatcher
from modules.file_reader import FileReader
from modules.interview_generator import InterviewGenerator
from modules.interview_scheduler import InterviewScheduler
from modules.pdf_generator import PDFGenerator
from modules.dashboard import Dashboard
from modules.airtable_manager import AirtableManager
from modules.gmail_reader import GmailReader
from modules.recruiter_review import RecruiterReview
from modules.recruiter_dashboard import RecruiterDashboard
import os

st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "candidate" not in st.session_state:
    st.session_state.candidate = None

if "match_json" not in st.session_state:
    st.session_state.match_json = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🤖 AI Recruitment")

page = st.sidebar.radio(
    "Navigation",
    [
        "Resume Analysis",
        "Import From Gmail",
        "Interview Questions",
        "Interview Scheduler",
        "Recruiter Review",
        "Recruiter Dashboard"
    ]
)

# =====================================================
# PAGE 1
# =====================================================

if page == "Resume Analysis":

    st.title("🤖 AI Recruitment System")

    st.markdown(
        "### AI Resume Screening & Interview Scheduling"
    )

    st.divider()

    resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

    if resume:

        parser = ResumeParser()

        text = parser.extract_text(resume)

        st.session_state.resume_text = text

        st.success("✅ Resume Uploaded Successfully!")

        with st.expander("View Resume"):

            st.text_area(
                "Resume",
                text,
                height=250
            )

        if st.button("🚀 Analyze Resume"):

            with st.spinner("Analyzing Resume..."):

                ai = AIExtractor()

                result = ai.extract_candidate(text)

                parser_json = JSONParser()

                candidate = parser_json.clean_json(result)

                reader = FileReader()

                jd = reader.read_job_description()

                matcher = JDMatcher()

                match_result = matcher.compare(
                    text,
                    jd
                )

            match_json = parser_json.clean_json(match_result)

# -----------------------------
# Automatic Shortlisting Logic
# -----------------------------

            score = str(match_json.get("match_score", "0"))
            score = score.replace("%", "").strip()

            try:
                score = int(float(score))
            except:
                score = 0

            if score >= 80:
                status = "Shortlisted"
            elif score >= 60:
                status = "Manual Review"
            else:
             status = "Rejected"

            match_json["application_status"] = status

            airtable = AirtableManager()
            airtable.save_candidate(candidate, match_json, resume.name)
            st.success("✅ Candidate saved to Airtable successfully!")
            st.session_state.candidate = candidate
            st.session_state.match_json = match_json

    if st.session_state.candidate is not None:

        candidate = st.session_state.candidate
        match_json = st.session_state.match_json

        st.success("Analysis Completed!")

        st.divider()
                # ============================================
        # Candidate Profile
        # ============================================

        st.header("👤 Candidate Profile")

        left, right = st.columns(2)

        with left:

            st.subheader("Basic Details")

            st.write("**Name:**", candidate.get("candidate_name", "N/A"))
            st.write("**Email:**", candidate.get("email", "N/A"))
            st.write("**Phone:**", candidate.get("phone", "N/A"))

            location = candidate.get("location", "N/A")

            if isinstance(location, list):
                location = ", ".join(location)

            st.write("**Location:**", location)

        with right:

            st.subheader("Professional Details")

            st.write(
                "**Experience:**",
                candidate.get("total_experience", "N/A")
            )

            languages = candidate.get("languages", [])

            if isinstance(languages, list):
                languages = ", ".join(languages)

            st.write("**Languages:**", languages)

        # ============================================
        # Education
        # ============================================

        st.subheader("🎓 Education")

        education = candidate.get("education", [])

        if isinstance(education, list):

            for edu in education:

                if isinstance(edu, dict):

                    st.info(
                        f"""
**Degree:** {edu.get('degree','N/A')}

**Institution:** {edu.get('institution','N/A')}
"""
                    )

                else:

                    st.info(str(edu))

        # ============================================
        # Dashboard
        # ============================================

        st.header("📊 Resume Match Dashboard")

        dashboard = Dashboard()
        dashboard.show(match_json)

        score = str(match_json.get("match_score", "0"))

        score = score.replace("%", "").strip()

        try:
            score = int(score)
        except:
            score = 0

        matching = match_json.get("matching_skills", [])
        missing = match_json.get("missing_skills", [])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🎯 Match Score", f"{score}%")

        with col2:
            st.metric("✅ Matching Skills", len(matching))

        with col3:
            st.metric("❌ Missing Skills", len(missing))

        st.progress(score / 100)

        st.subheader("✅ Matching Skills")

        for skill in matching:
            st.success(skill)

        st.subheader("❌ Missing Skills")

        for skill in missing:
            st.error(skill)

        st.subheader("🤖 AI Summary")

        st.info(
            match_json.get(
                "summary",
                "No Summary Available"
            )
        )

        st.subheader("📢 Hiring Recommendation")

        if score >= 80:
            st.success("✅ Candidate Shortlisted")

        elif score >= 60:
            st.warning("🟡 Needs Manual Review")

        else:
            st.error("❌ Rejected")

        pdf = PDFGenerator()

        pdf_file = pdf.generate(
            candidate,
            match_json
        )

        with open(pdf_file, "rb") as file:

            st.download_button(
                "📄 Download Candidate Report",
                file,
                file_name="Candidate_Report.pdf",
                mime="application/pdf"
            )
# ==========================================================
# PAGE - Import From Gmail
# ==========================================================

elif page == "Import From Gmail":

    st.title("📥 Import Resume From Gmail")

    if st.button("Download & Process Resume"):

        gmail = GmailReader()

        with st.spinner("Checking Gmail..."):
            filepath = gmail.get_latest_resume_email()

        if filepath is None:
            st.warning("No resume found in Gmail.")
            st.stop()

        parser = ResumeParser()
        ai = AIExtractor()
        json_parser = JSONParser()
        matcher = JDMatcher()
        reader = FileReader()
        airtable = AirtableManager()
        pdf = PDFGenerator()

        jd = reader.read_job_description()

        try:

            text = parser.extract_text(filepath)

            candidate_json = ai.extract_candidate(text)
            candidate = json_parser.clean_json(candidate_json)

            match_result = matcher.compare(text, jd)
            match_json = json_parser.clean_json(match_result)

            score = str(match_json.get("match_score", "0"))
            score = score.replace("%", "").strip()

            try:
                score = int(float(score))
            except:
                score = 0

            if score >= 80:
                match_json["application_status"] = "Shortlisted"
            elif score >= 60:
                match_json["application_status"] = "Manual Review"
            else:
                match_json["application_status"] = "Rejected"

            airtable.save_candidate(
                candidate,
                match_json,
                os.path.basename(filepath)
            )

            pdf.generate(candidate, match_json)

            st.success("✅ Resume processed successfully!")

        except Exception as e:
            st.error("Error processing resume.")
            st.exception(e)
            # ==========================================================
# PAGE 2 - Interview Questions
# ==========================================================

elif page == "Interview Questions":

    st.title("🎤 AI Interview Questions")

    if st.session_state.resume_text == "":

        st.warning("⚠️ Please analyze a resume first.")

    else:

        if st.button("Generate Interview Questions"):

            generator = InterviewGenerator()

            with st.spinner("Generating Interview Questions..."):

                questions = generator.generate(
                    st.session_state.resume_text
                )

            st.markdown(questions)


# ==========================================================
# PAGE 3 - Interview Scheduler
# ==========================================================

elif page == "Interview Scheduler":

    st.title("📅 Interview Scheduler")

    candidate = st.session_state.get("candidate", {})

    scheduler = InterviewScheduler()

    scheduler.schedule(candidate)
# ==========================================================
# PAGE 4 - Recruiter Review
# ==========================================================

elif page == "Recruiter Review":

    st.title("👨‍💼 Recruiter Review")

    if st.session_state.candidate is None:
        st.warning("⚠️ Please analyze a resume first.")
    else:
        reviewer = RecruiterReview()

        updated_candidate = reviewer.show(
            st.session_state.candidate
        )

        st.session_state.candidate = updated_candidate
elif page == "Recruiter Dashboard":

    dashboard = RecruiterDashboard()

    dashboard.show()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Developed by Shakeel Irfan | AI Recruitment System | 2026"
)