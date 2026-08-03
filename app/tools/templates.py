"""
Resume template registry -- 15 templates across 6 real structural
treatments (banner headers, accent bars, boxed summary, mono labels,
underlines, plain), not just color variants. All single-column and
ATS-safe.
"""

TEMPLATES = {
    "classic": {"name": "Classic", "description": "Traditional serif, thin rule headers -- safe and formal.",
        "accent": "#1E2A28", "font_body": "Times-Roman", "font_bold": "Times-Bold",
        "name_align": "CENTER", "header_style": "underline", "spacing": "normal"},
    "modern_minimal": {"name": "Modern Minimal", "description": "Sans-serif, no rules, generous whitespace.",
        "accent": "#4B5A57", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "plain", "spacing": "airy"},
    "executive": {"name": "Executive", "description": "Serif, navy accent, rule below each header -- senior feel.",
        "accent": "#1B3A5C", "font_body": "Times-Roman", "font_bold": "Times-Bold",
        "name_align": "CENTER", "header_style": "rule_below", "spacing": "normal"},
    "technical": {"name": "Technical", "description": "Monospace section headers -- engineering roles.",
        "accent": "#2E6B6B", "font_body": "Helvetica", "font_bold": "Helvetica-Bold", "font_mono": "Courier-Bold",
        "name_align": "LEFT", "header_style": "mono_label", "spacing": "normal"},
    "banner_navy": {"name": "Banner Navy", "description": "Bold navy header band behind your name.",
        "accent": "#1B3A5C", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "banner", "spacing": "normal"},
    "banner_forest": {"name": "Banner Forest", "description": "Deep green header band, serif body.",
        "accent": "#2F4A3C", "font_body": "Times-Roman", "font_bold": "Times-Bold",
        "name_align": "LEFT", "header_style": "banner", "spacing": "normal"},
    "banner_burgundy": {"name": "Banner Burgundy", "description": "Rich burgundy header band -- distinguished feel.",
        "accent": "#5C2430", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "banner", "spacing": "normal"},
    "banner_slate": {"name": "Banner Slate", "description": "Charcoal-slate header band -- modern, versatile.",
        "accent": "#2A3439", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "banner", "spacing": "normal"},
    "accent_teal": {"name": "Accent Bar Teal", "description": "Colored bar beside each heading, boxed summary.",
        "accent": "#2E6B6B", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "accent_bar", "spacing": "normal"},
    "accent_brass": {"name": "Accent Bar Brass", "description": "Warm brass accent bars, boxed summary.",
        "accent": "#96692A", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "accent_bar", "spacing": "normal"},
    "accent_plum": {"name": "Accent Bar Plum", "description": "Deep plum accent bars -- distinctive, not loud.",
        "accent": "#5A3E5C", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "accent_bar", "spacing": "normal"},
    "accent_crimson": {"name": "Accent Bar Crimson", "description": "Bold crimson accent bars -- stands out.",
        "accent": "#A6432E", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "accent_bar", "spacing": "normal"},
    "ivy_league": {"name": "Ivy League", "description": "Deep maroon serif, centered -- academic/law-firm look.",
        "accent": "#7A2E2E", "font_body": "Times-Roman", "font_bold": "Times-Bold",
        "name_align": "CENTER", "header_style": "rule_below", "spacing": "normal"},
    "consulting_classic": {"name": "Consulting Classic", "description": "Charcoal serif, centered, compact.",
        "accent": "#2B2B2B", "font_body": "Times-Roman", "font_bold": "Times-Bold",
        "name_align": "CENTER", "header_style": "underline", "spacing": "compact"},
    "sharp_corporate": {"name": "Sharp Corporate", "description": "Dense, bold, near-black -- senior applicants.",
        "accent": "#141414", "font_body": "Helvetica", "font_bold": "Helvetica-Bold",
        "name_align": "LEFT", "header_style": "underline", "spacing": "compact"},
}

DEFAULT_TEMPLATE = "classic"


def list_templates():
    return [
        {"id": tid, "name": t["name"], "description": t["description"], "accent": t["accent"]}
        for tid, t in TEMPLATES.items()
    ]


def get_template(template_id: str) -> dict:
    return TEMPLATES.get(template_id, TEMPLATES[DEFAULT_TEMPLATE])
