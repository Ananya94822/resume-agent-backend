"""
Tool 7: PDF generator
Takes structured resume JSON (from parse, build, or tailor) and produces
a clean, single-column, ATS-friendly PDF.
"""
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_CENTER


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="NameHeader", fontSize=18, spaceAfter=2, alignment=TA_CENTER, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="ContactLine", fontSize=9, alignment=TA_CENTER, spaceAfter=12, textColor="#444444"))
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=12, spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold", textColor="#1a1a1a"))
    styles.add(ParagraphStyle(name="EntryTitle", fontSize=10.5, fontName="Helvetica-Bold", spaceAfter=0))
    styles.add(ParagraphStyle(name="EntryMeta", fontSize=9.5, textColor="#333333", spaceAfter=2))
    styles.add(ParagraphStyle(name="ResumeBullet", fontSize=9.5, leading=13))
    styles.add(ParagraphStyle(name="BodyTextSmall", fontSize=9.5, leading=13, spaceAfter=6))
    return styles


def generate_resume_pdf(resume_json: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
    )
    styles = _styles()
    story = []

    story.append(Paragraph(resume_json.get("name", ""), styles["NameHeader"]))
    contact_parts = [p for p in [
        resume_json.get("email", ""),
        resume_json.get("phone", ""),
        resume_json.get("linkedin", ""),
        resume_json.get("github", ""),
    ] if p]
    story.append(Paragraph(" | ".join(contact_parts), styles["ContactLine"]))

    if resume_json.get("summary"):
        story.append(Paragraph("SUMMARY", styles["SectionHeader"]))
        story.append(Paragraph(resume_json["summary"], styles["BodyTextSmall"]))

    if resume_json.get("skills"):
        story.append(Paragraph("SKILLS", styles["SectionHeader"]))
        story.append(Paragraph(", ".join(resume_json["skills"]), styles["BodyTextSmall"]))

    if resume_json.get("education"):
        story.append(Paragraph("EDUCATION", styles["SectionHeader"]))
        for ed in resume_json["education"]:
            line = f"{ed.get('degree', '')} -- {ed.get('institution', '')}"
            meta = " | ".join(p for p in [ed.get("year", ""), ed.get("cgpa_or_percentage", "")] if p)
            story.append(Paragraph(line, styles["EntryTitle"]))
            if meta:
                story.append(Paragraph(meta, styles["EntryMeta"]))
            story.append(Spacer(1, 4))

    if resume_json.get("experience"):
        story.append(Paragraph("EXPERIENCE", styles["SectionHeader"]))
        for exp in resume_json["experience"]:
            story.append(Paragraph(f"{exp.get('title', '')} -- {exp.get('company', '')}", styles["EntryTitle"]))
            if exp.get("duration"):
                story.append(Paragraph(exp["duration"], styles["EntryMeta"]))
            if exp.get("bullets"):
                story.append(ListFlowable(
                    [ListItem(Paragraph(b, styles["ResumeBullet"])) for b in exp["bullets"]],
                    bulletType="bullet", leftIndent=14, spaceBefore=2, bulletFontSize=8,
                ))
            story.append(Spacer(1, 6))

    if resume_json.get("projects"):
        story.append(Paragraph("PROJECTS", styles["SectionHeader"]))
        for proj in resume_json["projects"]:
            story.append(Paragraph(proj.get("name", ""), styles["EntryTitle"]))
            if proj.get("tech_used"):
                story.append(Paragraph(", ".join(proj["tech_used"]), styles["EntryMeta"]))
            if proj.get("bullets"):
                story.append(ListFlowable(
                    [ListItem(Paragraph(b, styles["ResumeBullet"])) for b in proj["bullets"]],
                    bulletType="bullet", leftIndent=14, spaceBefore=2, bulletFontSize=8,
                ))
            story.append(Spacer(1, 6))

    if resume_json.get("certifications"):
        story.append(Paragraph("CERTIFICATIONS", styles["SectionHeader"]))
        story.append(Paragraph(", ".join(resume_json["certifications"]), styles["BodyTextSmall"]))

    doc.build(story)
    return buffer.getvalue()
