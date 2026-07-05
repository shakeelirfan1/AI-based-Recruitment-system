from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def generate(self, candidate, match_json):

        file_name = "Candidate_Report.pdf"

        doc = SimpleDocTemplate(file_name)

        styles = getSampleStyleSheet()

        story = []

        story.append(Paragraph("<b>AI Recruitment Report</b>", styles["Title"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph(f"<b>Name:</b> {candidate.get('candidate_name','')}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Email:</b> {candidate.get('email','')}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Phone:</b> {candidate.get('phone','')}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Experience:</b> {candidate.get('total_experience','')}", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph(f"<b>Resume Match Score:</b> {match_json.get('match_score','')}%", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Matching Skills</b>", styles["Heading2"]))

        for skill in match_json.get("matching_skills", []):
            story.append(Paragraph("• " + skill, styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))

        for skill in match_json.get("missing_skills", []):
            story.append(Paragraph("• " + skill, styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>AI Summary</b>", styles["Heading2"]))
        story.append(Paragraph(match_json.get("summary",""), styles["BodyText"]))

        doc.build(story)

        return file_name