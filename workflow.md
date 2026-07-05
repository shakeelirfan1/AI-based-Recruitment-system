# AI Recruitment System Workflow

## Workflow Overview

1. User uploads a resume or imports it from Gmail.
2. Resume is parsed using AI.
3. Candidate information is extracted into structured JSON.
4. Resume is matched against the Job Description.
5. AI calculates the candidate match score.
6. Candidate information is stored in Airtable.
7. Recruiter reviews the candidate.
8. Interview questions are generated.
9. Interview can be scheduled using Google Calendar.
10. Candidate report is generated as a PDF.

---

## Workflow Type

This project implements the workflow directly in Python modules and Streamlit rather than using n8n.

The complete workflow is implemented programmatically and documented in the project architecture.