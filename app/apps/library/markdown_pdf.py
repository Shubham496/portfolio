"""
MYTHOS Universal Markdown-to-PDF Conversion Engine
Converts any technical article or note in app/content/ into a publication-grade,
printable A4 PDF with branded header, footer, metadata badge, and clean typography.
Main written text is rendered in high-contrast black and white, while theme colors
(Electric Blue #2563EB, Vivid Orange #F97316, Dark Navy #070B14) accentuate
underlines, section headers, badges, and dividing bars.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from fpdf import FPDF
from fpdf.html import HTML2FPDF
from fpdf.drawing import DeviceRGB
from fpdf.fonts import TextStyle
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


class MythosHTML2FPDF(HTML2FPDF):
    """
    Custom HTML-to-PDF renderer attaching MYTHOS theme colors to header underlines,
    titles, and badges while enforcing high-contrast black-and-white for body prose.
    """

    def __init__(self, pdf, *args, **kwargs):
        super().__init__(pdf, *args, **kwargs)

        # ── Theme Typography for Headings ──
        # H1: Dark Navy with 16pt bold
        self.tag_styles["h1"] = TextStyle(
            font_family="Helvetica",
            font_style="B",
            font_size_pt=15.5,
            color=DeviceRGB(7 / 255, 11 / 255, 20 / 255),  # Dark Navy #070B14
            b_margin=2.0,
        )
        # H2: Dark Slate with 12.5pt bold
        self.tag_styles["h2"] = TextStyle(
            font_family="Helvetica",
            font_style="B",
            font_size_pt=12.5,
            color=DeviceRGB(15 / 255, 23 / 255, 42 / 255),  # Slate 900
            b_margin=1.8,
        )
        # H3: Slate 800 with 10.0pt bold
        self.tag_styles["h3"] = TextStyle(
            font_family="Helvetica",
            font_style="B",
            font_size_pt=10.0,
            color=DeviceRGB(30 / 255, 41 / 255, 59 / 255),  # Slate 800
            b_margin=1.5,
        )
        # H4: Slate 700 with 9.0pt bold
        self.tag_styles["h4"] = TextStyle(
            font_family="Helvetica",
            font_style="B",
            font_size_pt=9.0,
            color=DeviceRGB(51 / 255, 65 / 255, 85 / 255),
            b_margin=1.2,
        )

        # ── High-Contrast Black & White for Main Written Content ──
        # Paragraphs: Pure Black on White
        self.tag_styles["p"] = TextStyle(
            font_family="Helvetica",
            font_style="",
            font_size_pt=8.8,
            color=DeviceRGB(0, 0, 0),  # Pure Black for maximum print contrast
            b_margin=2.2,
        )
        # Monospace Code Blocks: Crisp Black on light background
        self.tag_styles["pre"] = TextStyle(
            font_family="Courier",
            font_style="",
            font_size_pt=7.2,
            color=DeviceRGB(0, 0, 0),
            b_margin=2.5,
        )
        self.tag_styles["code"] = TextStyle(
            font_family="Courier",
            font_style="",
            font_size_pt=7.2,
            color=DeviceRGB(0, 0, 0),
        )

    def handle_endtag(self, tag: str):
        super().handle_endtag(tag)

        # ── Theme Underlines Under Headers & Titles ──
        if tag == "h1":
            # H1: Split theme underline (Electric Blue + Vivid Orange + subtle slate baseline)
            y = self.pdf.get_y()
            self.pdf.set_fill_color(37, 99, 235)  # Electric Blue #2563EB
            self.pdf.rect(15, y, 55, 1.0, "F")
            self.pdf.set_fill_color(249, 115, 22)  # Vivid Orange #F97316
            self.pdf.rect(70, y, 20, 1.0, "F")
            self.pdf.set_fill_color(226, 232, 240)  # Slate 200
            self.pdf.rect(90, y, 105, 0.3, "F")
            self.pdf.set_y(y + 3.0)

        elif tag == "h2":
            # H2: Electric Blue line with Vivid Orange accent pip
            y = self.pdf.get_y()
            self.pdf.set_fill_color(249, 115, 22)  # Vivid Orange accent pip
            self.pdf.rect(15, y, 12, 0.8, "F")
            self.pdf.set_draw_color(37, 99, 235)   # Electric Blue line
            self.pdf.set_line_width(0.5)
            self.pdf.line(28, y + 0.4, 195, y + 0.4)
            self.pdf.set_y(y + 2.5)

        elif tag == "h3":
            # H3: Subtle slate baseline separator
            y = self.pdf.get_y()
            self.pdf.set_draw_color(203, 213, 225)  # Slate 300
            self.pdf.set_line_width(0.3)
            self.pdf.line(15, y, 195, y)
            self.pdf.set_y(y + 1.8)


class MythosNotePDF(FPDF):
    """Publication-grade A4 PDF canvas with MYTHOS dark navy header and institutional footer."""

    HTML2FPDF_CLASS = MythosHTML2FPDF

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
    pdf.set_text_color(7, 11, 20)  # Dark Navy #070B14
    pdf.multi_cell(0, 6.8, sanitized_title, align="L")
    pdf.ln(1)

    # Metadata Strip (Theme Accents)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(37, 99, 235)  # Electric Blue #2563EB
    meta_line = f"CATEGORY: {sanitized_cat.upper()}   |   READING TIME: {reading_time.upper()}"
    if sanitized_tags:
        meta_line += f"   |   TAGS: {sanitized_tags.upper()}"
    pdf.cell(0, 4.5, meta_line, align="L", new_x="LMARGIN", new_y="NEXT")

    # Title Split Accent Underline
    y_div = pdf.get_y() + 1.0
    pdf.set_fill_color(37, 99, 235)  # Electric Blue
    pdf.rect(15, y_div, 60, 1.2, "F")
    pdf.set_fill_color(249, 115, 22)  # Vivid Orange
    pdf.rect(75, y_div, 25, 1.2, "F")
    pdf.set_fill_color(226, 232, 240)  # Slate 200
    pdf.rect(100, y_div, 95, 0.4, "F")
    pdf.set_y(y_div + 4.5)

    # 6. Render Body HTML with MythosHTML2FPDF
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
