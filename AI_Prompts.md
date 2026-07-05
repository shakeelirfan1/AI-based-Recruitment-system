# AI Prompts Used

## 1. Resume Information Extraction

### Objective
Extract structured candidate information from the uploaded resume.

### Prompt

Extract the following information from the resume and return only valid JSON.

Fields:
- Candidate Name
- Email
- Phone Number
- Location
- Current Role
- Current Company
- Total Experience
- Education
- Technical Skills
- Soft Skills
- Certifications
- Languages
- Projects

Return only JSON.

---

## 2. Job Description Matching

### Objective

Compare the extracted resume information with the Job Description.

### Prompt

Compare the candidate resume with the provided Job Description.

Generate:

- Match Score (0–100)
- Matching Skills
- Missing Skills
- AI Summary
- Recommendation

Return only JSON.

---

## 3. Interview Question Generation

### Objective

Generate personalized interview questions.

### Prompt

Generate 10 technical interview questions based on:

- Candidate Skills
- Experience
- Job Description

Include:
- Difficulty
- Expected Answer
- Topic

Return JSON.