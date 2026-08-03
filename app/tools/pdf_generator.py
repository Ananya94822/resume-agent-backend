"""
Tool 7: PDF generator
Renders structured resume JSON into a clean, ATS-friendly PDF. Templates
vary structurally, not just in color.
"""
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors as rl_colors

from app.tools.templates import get_template

_JUNK_VALUES = {"not specified", "n/a", "na", "tbd", "unknown", "none", "-", ""}


def _clean(value):
    if not value:
        return ""
    if str(value).strip().lower() in _JUNK_VALUES:
        return ""
    return str(value).strip()


def _styles(tpl, banner_mode=False):
    styles = getSampleStyleSheet()
    accent = tpl["accent"]
    body_font = tpl["font_body"]
    bold_font = tpl["font_bold"]
    name_align = TA_CENTER if tpl["name_align"] == "CENTER" else TA_LEFT
    spacing = tpl["spacing"]

    section_space_before = {"compact": 6, "normal": 10, "airy": 16}[spacing]
    body_leading = {"compact": 11.5, "normal": 13, "airy": 14.5}[spacing]

    name_color = "#FFFFFF" if banner_mode else "#1E2A28"
    contact_color = "#F0F0F0" if banner_mode else "#4B5A57"

    styles.add(ParagraphStyle(name="NameHeader", fontName=bold_font, fontSize=19, leading=23,
                               alignment=name_align, spaceAfter=2, textColor=name_color))
    styles.add(ParagraphStyle(name="ContactLine", fontName=body_font, fontSize=9, leading=12,
                               alignment=name_align, spaceAfter=0 if banner_mode else 14, textColor=contact_color))
    styles.add(ParagraphStyle(name="SectionHeader", fontName=bold_font, fontSize=11.5, leading=14,
                               spaceBefore=section_space_before, spaceAfter=5, textColor=accent))
    styles.add(ParagraphStyle(name="SectionHeaderBar", fontName=bold_font, fontSize=11, leading=13,
                               textColor="#1E2A28"))
    styles.add(ParagraphStyle(name="EntryTitle", fontName=bold_font, fontSize=10.5, leading=13, spaceAfter=0))
    styles.add(ParagraphStyle(name="EntryMeta", fontName=body_font, fontSize=9.5, leading=12,
                               textColor="#444444", spaceAfter=2))
    styles.add(ParagraphStyle(name="ResumeBullet", fontName=body_font, fontSize=9.5, leading=body_leading))
    styles.add(ParagraphStyle(name="BodyTextSmall", fontName=body_font, fontSize=9.5,
                               leading=body_leading, spaceAfter=6))
    styles.add(ParagraphStyle(name="BoxedSummary", fontName=body_font, fontSize=9.5,
                               leading=body_leading, textColor="#1E2A28"))
    styles.add(ParagraphStyle(name="MonoLabel", fontName=tpl.get("font_mono", bold_font), fontSize=8.5, leading=11,
                               textColor=accent, spaceAfter=4))
    return styles


def _section_header(text, styles, tpl, story):
    style = tpl["header_style"]
    if style == "mono_label":
        story.append(Paragraph(f"// {text}", styles["MonoLabel"]))
    elif style == "accent_bar":
        bar_table = Table(
            [[Paragraph("&nbsp;", styles["SectionHeaderBar"]), Paragraph(text.upper(), styles["SectionHeaderBar"])]],
            colWidths=[5, None],
        )
        bar_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), rl_colors.HexColor(tpl["accent"])),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), 0),
            ("LEFTPADDING", (1, 0), (1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(Spacer(1, 8))
        story.append(bar_table)
        story.append(Spacer(1, 4))
    else:
        story.append(Paragraph(text.upper(), styles["SectionHeader"]))
    if style == "underline":
        story.append(Paragraph(
            f'<font color="{tpl["accent"]}">{"_" * 34}</font>', styles["EntryMeta"]))


def _build_header(resume_json, styles, tpl, story):
    name = _clean(resume_json.get("name")) or "Your Name"
    contact_parts = [p for p in [
        _clean(resume_json.get("email")), _clean(resume_json.get("phone")),
        _clean(resume_json.get("linkedin")), _clean(resume_json.get("github")),
    ] if p]
    contact_line = " | ".join(contact_parts)

    if tpl["header_style"] == "banner":
        cell_content = [Paragraph(name, styles["NameHeader"])]
        if contact_line:
            cell_content.append(Paragraph(contact_line, styles["ContactLine"]))
        banner = Table([[cell_content]], colWidths=[None])
        banner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), rl_colors.HexColor(tpl["accent"])),
            ("TOPPADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
            ("LEFTPADDING", (0, 0), (-1, -1), 20),
            ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ]))
        story.append(banner)
        story.append(Spacer(1, 14))
    else:
        story.append(Paragraph(name, styles["NameHeader"]))
        if contact_line:
            story.append(Paragraph(contact_line, styles["ContactLine"]))
        else:
            story.append(Spacer(1, 10))


def generate_resume_pdf(resume_json: dict, template_id: str = "classic") -> bytes:
    tpl = get_template(template_id)
    banner_mode = tpl["header_style"] == "banner"
    buffer = io.BytesIO()
    margin = 0.55 * inch if tpl["spacing"] == "compact" else 0.7 * inch
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=(0.0 if banner_mode else 0.55 * inch), bottomMargin=0.55 * inch,
        leftMargin=margin, rightMargin=margin,
    )
    styles = _styles(tpl, banner_mode=banner_mode)
    story = []

    _build_header(resume_json, styles, tpl, story)

    summary = _clean(resume_json.get("summary"))
    if summary:
        if tpl["header_style"] == "accent_bar":
            box = Table([[Paragraph(summary, styles["BoxedSummary"])]], colWidths=[None])
            box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), rl_colors.HexColor("#F6F4EF")),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]))
            story.append(box)
            story.append(Spacer(1, 4))
        else:
            _section_header("Summary", styles, tpl, story)
            story.append(Paragraph(summary, styles["BodyTextSmall"]))

    skills = [s for s in (resume_json.get("skills") or []) if _clean(s)]
    if skills:
        _section_header("Skills", styles, tpl, story)
        story.append(Paragraph(", ".join(skills), styles["BodyTextSmall"]))

    education = [ed for ed in (resume_json.get("education") or [])
                 if _clean(ed.get("degree")) or _clean(ed.get("institution"))]
    if education:
        _section_header("Education", styles, tpl, story)
        for ed in education:
            degree = _clean(ed.get("degree"))
            institution = _clean(ed.get("institution"))
            line = " -- ".join([p for p in [degree, institution] if p])
            meta = " | ".join(p for p in [_clean(ed.get("year")), _clean(ed.get("cgpa_or_percentage"))] if p)
            if line:
                story.append(Paragraph(line, styles["EntryTitle"]))
            if meta:
                story.append(Paragraph(meta, styles["EntryMeta"]))
            story.append(Spacer(1, 4))

    experience = [e for e in (resume_json.get("experience") or [])
                  if _clean(e.get("title")) or _clean(e.get("company"))]
    if experience:
        _section_header("Experience", styles, tpl, story)
        for exp in experience:
            title = _clean(exp.get("title"))
            company = _clean(exp.get("company"))
            line = " -- ".join([p for p in [title, company] if p])
            if line:
                story.append(Paragraph(line, styles["EntryTitle"]))
            duration = _clean(exp.get("duration"))
            if duration:
                story.append(Paragraph(duration, styles["EntryMeta"]))
            bullets = [b for b in (exp.get("bullets") or []) if _clean(b)]
            if bullets:
                story.append(ListFlowable(
                    [ListItem(Paragraph(b, styles["ResumeBullet"])) for b in bullets],
                    bulletType="bullet", leftIndent=14, spaceBefore=2, bulletFontSize=8,
                ))
            story.append(Spacer(1, 6))

    projects = [p for p in (resume_json.get("projects") or []) if _clean(p.get("name"))]
    if projects:
        _section_header("Projects", styles, tpl, story)
        for proj in projects:
            name_p = _clean(proj.get("name"))
            if name_p:
                story.append(Paragraph(name_p, styles["EntryTitle"]))
            tech = [t for t in (proj.get("tech_used") or []) if _clean(t)]
            if tech:
                story.append(Paragraph(", ".join(tech), styles["EntryMeta"]))
            bullets = [b for b in (proj.get("bullets") or []) if _clean(b)]
            if bullets:
                story.append(ListFlowable(
                    [ListItem(Paragraph(b, styles["ResumeBullet"])) for b in bullets],
                    bulletType="bullet", leftIndent=14, spaceBefore=2, bulletFontSize=8,
                ))
            story.append(Spacer(1, 6))

    certs = [c for c in (resume_json.get("certifications") or []) if _clean(c)]
    if certs:
        _section_header("Certifications", styles, tpl, story)
        story.append(Paragraph(", ".join(certs), styles["BodyTextSmall"]))

    doc.build(story)
    return buffer.getvalue()
