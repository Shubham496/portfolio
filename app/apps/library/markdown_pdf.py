"""
MYTHOS Universal Markdown-to-PDF Conversion Engine
Converts any technical article or note in app/content/ into a publication-grade,
printable A4 PDF with branded header, footer, metadata badge, and clean typography.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from fpdf import FPDF
import markdown
import frontmatter

from app.core.config import settings


# Core font latin-1 character replacement dictionary
UNICODE_REPLACEMENTS = [
    ("\u2014", "--"),   # Em-dash
    ("\u2013", "-"),    # En-dash
    ("\u2018", "'"),    # Left single quote
    ("\u2019", "'"),    # Right single quote
    ("\u201c", '"'),    # Left double quote
    ("\u201d", '"'),    # Right double quote
    ("\u2022", "* "),   # Bullet point
    ("\u2026", "..."),  # Ellipsis
    ("\u2192", "->"),   # Right arrow
    ("\u2190", "<-"),   # Left arrow
    ("\u2194", "<->"),  # Left-right arrow
    ("\u20b9", "INR "), # Rupee symbol
    ("\u00a0", " "),    # Non-breaking space
]


class MythosNotePDF(FPDF):
    """Publication-grade A4 PDF canvas with MYTHOS dark navy header and institutional footer."""

    def __init__(self, doc_title: str = "", doc_subject: str = "", *args, **kwargs):
        super().__init__(orientation="P", unit="mm", format="A4", *args, **kwargs)
        self.doc_title = doc_title
        self.doc_subject = doc_subject.upper() if doc_subject else "DATA & ENGINEERING"
        # Standard A4 print margins: 15mm left/right gives 180mm printable width (epw)
        self.set_margins(15, 20, 15)
        self.set_auto_page_break(auto=True, margin=16)

    def header(self):
        # Top Dark Navy Banner (#070B14)
        self.set_fill_color(7, 11, 20)
        self.rect(0, 0, 210, 15, "F")

        # Top Accent Split Line (Electric Blue on left 125mm, Vivid Orange on right 85mm)
        self.set_fill_color(37, 99, 235)  # Electric Blue #2563EB
        self.rect(0, 15, 125, 1.2, "F")
        self.set_fill_color(249, 115, 22)  # Vivid Orange #F97316
        self.rect(125, 15, 85, 1.2, "F")

        # Header Text
        self.set_xy(15, 3.5)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(255, 255, 255)
        self.cell(100, 7.5, "MYTHOS | ONLINE EDUCATIONAL INSTITUTE", align="L")

        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(148, 163, 184)  # Slate 400
        header_tag = f"{self.doc_subject} | TECHNICAL STUDY NOTE"
        self.cell(80, 7.5, header_tag, align="R")
        self.ln(14)

    def footer(self):
        # Baseline separator bar
        self.set_y(-14)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())

        # Footer Text
        self.set_y(-12)
        self.set_font("Helvetica", "B", 7.0)
        self.set_text_color(37, 99, 235)
        self.cell(45, 6, "MYTHOS KNOWLEDGE ENGINE", align="L")

        self.set_font("Helvetica", "", 7.0)
        self.set_text_color(71, 85, 105)
        self.cell(105, 6, f"Admissions: {settings.BUSINESS_EMAIL} | WhatsApp: +91 {settings.BUSINESS_WHATSAPP}", align="C")

        self.set_font("Helvetica", "B", 7.0)
        self.set_text_color(100, 116, 139)
        self.cell(30, 6, f"Page {self.page_no()}", align="R")


def sanitize_text_for_pdf(text: str) -> str:
    """Replaces Unicode characters outside standard latin-1 encoding with clean ASCII equivalents."""
    for old, new in UNICODE_REPLACEMENTS:
        text = text.replace(old, new)
    # Filter any remaining character outside latin-1 to avoid FPDFUnicodeEncodingException
    return "".join(c if ord(c) < 256 else "?" for c in text)


def preprocess_markdown_alerts(text: str) -> str:
    """Converts GitHub admonition blocks (> [!NOTE], etc.) into clean HTML for write_html."""
    alert_patterns = [
        (r">\s*\[!NOTE\]\s*\n((?:>.*\n?)*)", r"<blockquote><b>NOTE:</b> \1</blockquote>"),
        (r">\s*\[!TIP\]\s*\n((?:>.*\n?)*)", r"<blockquote><b>TIP:</b> \1</blockquote>"),
        (r">\s*\[!IMPORTANT\]\s*\n((?:>.*\n?)*)", r"<blockquote><b>IMPORTANT:</b> \1</blockquote>"),
        (r">\s*\[!WARNING\]\s*\n((?:>.*\n?)*)", r"<blockquote><b>WARNING:</b> \1</blockquote>"),
        (r">\s*\[!CAUTION\]\s*\n((?:>.*\n?)*)", r"<blockquote><b>CAUTION:</b> \1</blockquote>"),
    ]
    for pattern, replacement in alert_patterns:
        def repl(match):
            inner = match.group(1).replace(">", "").strip()
            return f"\n<p><b>[{match.group(0).split(']')[0].replace('> [!', '').upper()}]:</b> {inner}</p>\n"
        text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    return text


def render_markdown_to_pdf(
    markdown_content: str,
    title: Optional[str] = None,
    subject: Optional[str] = None,
    output_path: Optional[str] = None,
) -> bytes:
    """
    Renders raw Markdown content into a branded, printable A4 PDF.
    Extracts frontmatter if present and outputs publication-grade layout.
    """
    # 1. Parse frontmatter if present
    post = frontmatter.loads(markdown_content)
    meta = post.metadata or {}
    raw_body = post.content

    resolved_title = title or meta.get("title") or "Technical Study Note"
    resolved_subject = subject or meta.get("subject") or "Engineering"
    category = meta.get("category", "Core Curriculum")
    reading_time = meta.get("reading_time", "8 min read")
    tags = meta.get("tags") or []
    if isinstance(tags, list):
        tags_str = " | ".join(str(t) for t in tags[:4])
    else:
        tags_str = str(tags)

    # 2. Sanitize body text
    sanitized_body = sanitize_text_for_pdf(raw_body)
    sanitized_title = sanitize_text_for_pdf(resolved_title)
    sanitized_cat = sanitize_text_for_pdf(category)
    sanitized_tags = sanitize_text_for_pdf(tags_str)

    # 3. Preprocess alerts and strip mermaid code blocks for clean print rendering
    clean_body = preprocess_markdown_alerts(sanitized_body)
    clean_body = re.sub(r"```mermaid[\s\S]*?```", "\n*[Visual Diagram: See Interactive Web Platform]*\n", clean_body)

    # 4. Convert markdown to HTML for fpdf2
    html_content = markdown.markdown(
        clean_body,
        extensions=["tables", "fenced_code"],
        output_format="html5",
    )

    # 5. Initialize PDF
    pdf = MythosNotePDF(doc_title=sanitized_title, doc_subject=resolved_subject)
    pdf.add_page()

    # Title & Metadata Banner
    pdf.set_y(22)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(15, 23, 42)  # Slate 900
    pdf.multi_cell(0, 7.0, sanitized_title, align="L")
    pdf.ln(1)

    # Metadata Strip
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(37, 99, 235)  # Blue 600
    meta_line = f"CATEGORY: {sanitized_cat.upper()}   |   READING TIME: {reading_time.upper()}"
    if sanitized_tags:
        meta_line += f"   |   TAGS: {sanitized_tags.upper()}"
    pdf.cell(0, 4.5, meta_line, align="L", new_x="LMARGIN", new_y="NEXT")

    # Divider line
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y() + 1.5, 195, pdf.get_y() + 1.5)
    pdf.set_y(pdf.get_y() + 4.0)

    # 6. Render Body HTML
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(30, 41, 59)  # Slate 800
    pdf.write_html(html_content)

    # 7. Output result
    pdf_bytes = bytes(pdf.output())
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes


def render_markdown_file_to_pdf(file_path: Path | str, output_path: Optional[str] = None) -> str:
    """Reads an authored Markdown file on disk and outputs a compiled, printable PDF."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Markdown file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    target_output = output_path or f"app/static/pdf/{path.parent.name}_{path.stem}.pdf"
    render_markdown_to_pdf(markdown_content=content, output_path=target_output)
    return target_output
