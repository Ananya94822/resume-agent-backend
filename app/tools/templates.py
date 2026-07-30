"""
Resume template registry. Every template is single-column, uses standard
built-in PDF fonts (no embedded/custom fonts), and differs only in
typography pairing, accent color, header treatment, and spacing.
"""

TEMPLATES = {
    "classic": {
        "name": "Classic",
        "description": "Traditional serif resume -- safe, formal, universally accepted.",
        "accent": "#1E2A28",
        "font_body": "Times-Roman",
        "font_bold": "Times-Bold",
        "name_align": "CENTER",
        "header_style": "underline",
        "spacing": "normal",
    },
    "modern_minimal": {
        "name": "Modern Minimal",
        "description": "Clean sans-serif, generous whitespace, understated.",
        "accent": "#4B5A57",
        "font_body": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "name_align": "LEFT",
        "header_style": "plain",
        "spacing": "airy",
    },
    "executive": {
        "name": "Executive",
        "description": "Serif with a navy accent -- senior, polished feel.",
        "accent": "#1B3A5C",
        "font_body": "Times-Roman",
        "font_bold": "Times-Bold",
        "name_align": "CENTER",
        "header_style": "rule_below",
        "spacing": "normal",
    },
    "clean_left": {
        "name": "Clean Left-Aligned",
        "description": "Sans-serif, left-aligned header, forest-green accent.",
        "accent": "#3F6355",
        "font_body": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "name_align": "LEFT",
        "header_style": "underline",
        "spacing": "normal",
    },
    "compact": {
        "name": "Compact",
        "description": "Tighter spacing -- fits more on one page for dense resumes.",
        "accent": "#96692A",
        "font_body": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "name_align": "CENTER",
        "header_style": "plain",
        "spacing": "compact",
    },
    "elegant_serif": {
        "name": "Elegant Serif",
        "description": "Refined serif, thin grey rules, quiet confidence.",
        "accent": "#6B6558",
        "font_body": "Times-Roman",
        "font_bold": "Times-Bold",
        "name_align": "CENTER",
        "header_style": "rule_below",
        "spacing": "airy",
    },
    "technical": {
        "name": "Technical",
        "description": "Sans-serif with monospace section labels -- built for engineering roles.",
        "accent": "#2E6B6B",
        "font_body": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "font_mono": "Courier-Bold",
        "name_align": "LEFT",
        "header_style": "mono_label",
        "spacing": "normal",
    },
    "bold_header": {
        "name": "Bold Header",
        "description": "Strong sans-serif name treatment, brick-red accent.",
        "accent": "#A6432E",
        "font_body": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "name_align": "LEFT",
        "header_style": "underline",
        "spacing": "normal",
    },
}

DEFAULT_TEMPLATE = "classic"


def list_templates():
    return [
        {"id": tid, "name": t["name"], "description": t["description"], "accent": t["accent"]}
        for tid, t in TEMPLATES.items()
    ]


def get_template(template_id: str) -> dict:
    return TEMPLATES.get(template_id, TEMPLATES[DEFAULT_TEMPLATE])
