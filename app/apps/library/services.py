"""
MYTHOS Knowledge & Resource Engine Services.
Handles Markdown discovery, YAML frontmatter parsing, TOC extraction,
caching, and subject metadata indexing.
"""

from __future__ import annotations

import os
import re
import math
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

import markdown
import frontmatter


# Path configuration
CONTENT_DIR = Path(__file__).resolve().parent.parent.parent / "content"

# Standard subjects metadata
SUBJECTS: Dict[str, Dict[str, Any]] = {
    "sql": {
        "slug": "sql",
        "title": "SQL & Relational Databases",
        "short_title": "SQL",
        "tagline": "From Textbook Theory to Production Query Engines",
        "description": "Comprehensive guides to relational database internals, non-equi joins, execution planners, indexing, and high-frequency viva/interview traps.",
        "icon": "database",
        "accent": "blue",
        "accent_hex": "#2563EB",
        "gradient": "from-blue-600 to-cyan-500",
        "badge": "Core Track",
    },
    "python": {
        "slug": "python",
        "title": "Python & Data Engineering",
        "short_title": "Python",
        "tagline": "Modern Python Internals, OOP & ETL Pipelines",
        "description": "In-depth explorations of Python memory management, mutable traps, generator pipelines, Pandas wrangling, and production automation.",
        "icon": "code-2",
        "accent": "amber",
        "accent_hex": "#F59E0B",
        "gradient": "from-amber-500 to-orange-500",
        "badge": "Core Track",
    },
    "bi": {
        "slug": "bi",
        "title": "Business Intelligence & Analytics",
        "short_title": "Power BI & Tableau",
        "tagline": "Star Schemas, Advanced DAX & Executive Storytelling",
        "description": "Fact/dimension modeling, complex DAX measures, Tableau LOD calculations, and real-world interactive BI dashboards.",
        "icon": "bar-chart-3",
        "accent": "emerald",
        "accent_hex": "#10B981",
        "gradient": "from-emerald-500 to-teal-500",
        "badge": "Core Track",
    },
    "digital-marketing": {
        "slug": "digital-marketing",
        "title": "Performance Marketing & Growth",
        "short_title": "Marketing",
        "tagline": "Paid Ad Scaling, SEO Funnels & CRO Architecture",
        "description": "Technical SEO audits, Meta Ads ROAS optimization, Google Ads PMax bidding algorithms, and multi-channel attribution.",
        "icon": "trending-up",
        "accent": "purple",
        "accent_hex": "#8B5CF6",
        "gradient": "from-purple-600 to-pink-500",
        "badge": "Specialization",
    },
}

# Standard verticals metadata
VERTICALS: Dict[str, Dict[str, Any]] = {
    "notes": {
        "slug": "notes",
        "title": "Comprehensive Notes",
        "singular": "Note",
        "icon": "file-text",
        "badge": "Free & In-Depth",
    },
    "viva": {
        "slug": "viva",
        "title": "Practice & Viva Banks",
        "singular": "Viva Bank",
        "icon": "help-circle",
        "badge": "Exam & Viva Q&A",
    },
    "datasets": {
        "slug": "datasets",
        "title": "Practice Datasets",
        "singular": "Dataset",
        "icon": "layers",
        "badge": "Portfolio Ready",
    },
    "books": {
        "slug": "books",
        "title": "Books & Handbooks",
        "singular": "Handbook",
        "icon": "book-open",
        "badge": "Complete Guide",
    },
    "projects": {
        "slug": "projects",
        "title": "Capstone Projects",
        "singular": "Capstone",
        "icon": "rocket",
        "badge": "Production Code",
    },
}


@dataclass
class DocumentMetadata:
    title: str
    slug: str
    subject: str
    vertical: str = "notes"
    category: str = "General"
    order: int = 999
    tier: str = "free"
    price_inr: int = 0
    reading_time: str = "5 min read"
    description: str = ""
    tags: List[str] = field(default_factory=list)
    last_updated: str = ""
    file_path: Optional[str] = None
    mtime: float = 0.0

    @property
    def is_free(self) -> bool:
        return self.price_inr == 0 or self.tier == "free"

    @property
    def access_label(self) -> str:
        """Zero-upfront pricing label: price is only shown on paywall block or purchase click."""
        if self.is_free:
            return "Free Access"
        if self.tier == "student_login":
            return "Student Account"
        if self.vertical == "viva":
            return "Viva Bank"
        if self.vertical == "books":
            return "Complete Handbook"
        if self.vertical == "projects":
            return "Capstone Repo"
        return "Full Resource"

    @property
    def formatted_price(self) -> str:
        """Internal/Paywall-only price display."""
        if self.price_inr == 0:
            return "Free"
        return f"₹{self.price_inr}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "slug": self.slug,
            "subject": self.subject,
            "vertical": self.vertical,
            "category": self.category,
            "order": self.order,
            "tier": self.tier,
            "price_inr": self.price_inr,
            "access_label": self.access_label,
            "formatted_price": self.formatted_price,
            "reading_time": self.reading_time,
            "description": self.description,
            "tags": self.tags,
            "last_updated": self.last_updated,
            "is_free": self.is_free,
        }


@dataclass
class ParsedDocument:
    metadata: DocumentMetadata
    html_content: str
    toc_tokens: List[Dict[str, Any]]
    toc_html: str
    raw_content: str


# In-memory document and metadata cache:
# Cache key: (subject, slug) -> (mtime, ParsedDocument)
_DOCUMENT_CACHE: Dict[tuple, tuple[float, ParsedDocument]] = {}
_SUBJECT_DOCS_CACHE: Dict[str, tuple[float, List[DocumentMetadata]]] = {}


def _preprocess_github_alerts(text: str) -> str:
    """
    Transforms GitHub-style alerts:
      > [!NOTE]
      > Alert content
    into standard Python-Markdown admonitions:
      !!! note
          Alert content
    """
    pattern = re.compile(
        r">\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION|EXAM|PRO-TIP)\]\s*\n((?:>[^\n]*\n?)*)",
        re.IGNORECASE,
    )

    def _replace(match: re.Match) -> str:
        tag = match.group(1).lower().replace("-", "")
        if tag in ("pro-tip", "protip"):
            tag = "tip"
        elif tag in ("exam",):
            tag = "warning"
        body = match.group(2)
        # Strip leading '>' and up to one space from each line
        indented_body = re.sub(r"^>\s?", "    ", body, flags=re.MULTILINE)
        return f'!!! {tag}\n{indented_body}\n'

    return pattern.sub(_replace, text)


def _calculate_reading_time(word_count: int, wpm: int = 200) -> str:
    minutes = max(1, math.ceil(word_count / wpm))
    return f"{minutes} min read"


def _build_markdown_parser() -> markdown.Markdown:
    """Configures Markdown parser with PyMdown extensions and TOC."""
    return markdown.Markdown(
        extensions=[
            "tables",
            "admonition",
            "pymdownx.superfences",
            "pymdownx.highlight",
            "pymdownx.tabbed",
            "pymdownx.tasklist",
            "pymdownx.betterem",
            "pymdownx.caret",
            "pymdownx.mark",
            "pymdownx.tilde",
            "toc",
        ],
        extension_configs={
            "pymdownx.highlight": {
                "use_pygments": False,
                "css_class": "code-block",
            },
            "pymdownx.superfences": {
                "css_class": "code-block-wrapper",
            },
            "toc": {
                "permalink": False,
                "baselevel": 2,
            },
        },
    )


def parse_markdown_file(file_path: Path) -> ParsedDocument:
    """Parses a single markdown file with frontmatter into ParsedDocument."""
    with open(file_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    meta = post.metadata or {}
    slug = meta.get("slug") or file_path.stem
    subject = meta.get("subject") or file_path.parent.name
    title = meta.get("title") or slug.replace("-", " ").title()
    category = meta.get("category", "General")
    vertical = meta.get("vertical", "notes")
    order = int(meta.get("order", 999))
    tier = meta.get("tier", "free")
    price_inr = int(meta.get("price_inr", 0))
    tags = meta.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    last_updated = meta.get("last_updated", "")

    raw_body = post.content
    words = len(raw_body.split())
    reading_time = meta.get("reading_time") or _calculate_reading_time(words)
    description = meta.get("description", "")
    if not description and raw_body:
        # First non-header paragraph fallback
        paragraphs = [p.strip() for p in raw_body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
        if paragraphs:
            description = paragraphs[0][:160] + "..."

    doc_meta = DocumentMetadata(
        title=title,
        slug=slug,
        subject=subject,
        vertical=vertical,
        category=category,
        order=order,
        tier=tier,
        price_inr=price_inr,
        reading_time=reading_time,
        description=description,
        tags=tags,
        last_updated=str(last_updated),
        file_path=str(file_path),
        mtime=file_path.stat().st_mtime,
    )

    # Convert Markdown to HTML
    preprocessed_body = _preprocess_github_alerts(raw_body)
    md = _build_markdown_parser()
    html_content = md.convert(preprocessed_body)
    toc_tokens = getattr(md, "toc_tokens", [])
    toc_html = getattr(md, "toc", "")

    return ParsedDocument(
        metadata=doc_meta,
        html_content=html_content,
        toc_tokens=toc_tokens,
        toc_html=toc_html,
        raw_content=raw_body,
    )


def get_document(subject: str, slug: str) -> Optional[ParsedDocument]:
    """
    Retrieves a parsed document by subject and slug with in-memory caching.
    Invalidates automatically if the on-disk file has been updated.
    """
    subject_dir = CONTENT_DIR / subject
    if not subject_dir.exists():
        return None

    # Search for matching file
    target_file = None
    for file_path in subject_dir.glob("*.md"):
        if file_path.stem == slug:
            target_file = file_path
            break
        # Also check frontmatter slug if stem does not match
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
                if post.metadata.get("slug") == slug:
                    target_file = file_path
                    break
        except Exception:
            continue

    if not target_file or not target_file.is_file():
        return None

    mtime = target_file.stat().st_mtime
    cache_key = (subject, slug)

    if cache_key in _DOCUMENT_CACHE:
        cached_mtime, cached_doc = _DOCUMENT_CACHE[cache_key]
        if cached_mtime == mtime:
            return cached_doc

    parsed = parse_markdown_file(target_file)
    _DOCUMENT_CACHE[cache_key] = (mtime, parsed)
    return parsed


def list_documents_for_subject(
    subject: str, vertical: Optional[str] = None
) -> List[DocumentMetadata]:
    """
    Lists all documents for a given subject, sorted by category and order.
    Optionally filters by vertical (e.g. 'notes', 'viva', 'datasets').
    """
    subject_dir = CONTENT_DIR / subject
    if not subject_dir.exists():
        return []

    docs: List[DocumentMetadata] = []
    for file_path in subject_dir.glob("*.md"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
            meta = post.metadata or {}
            slug = meta.get("slug") or file_path.stem
            doc_vertical = meta.get("vertical", "notes")
            if vertical and doc_vertical != vertical:
                continue

            order = int(meta.get("order", 999))
            title = meta.get("title") or slug.replace("-", " ").title()
            category = meta.get("category", "General")
            tier = meta.get("tier", "free")
            price_inr = int(meta.get("price_inr", 0))
            tags = meta.get("tags") or []
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]

            words = len(post.content.split())
            reading_time = meta.get("reading_time") or _calculate_reading_time(words)
            description = meta.get("description", "")

            doc_meta = DocumentMetadata(
                title=title,
                slug=slug,
                subject=subject,
                vertical=doc_vertical,
                category=category,
                order=order,
                tier=tier,
                price_inr=price_inr,
                reading_time=reading_time,
                description=description,
                tags=tags,
                last_updated=str(meta.get("last_updated", "")),
                file_path=str(file_path),
                mtime=file_path.stat().st_mtime,
            )
            docs.append(doc_meta)
        except Exception:
            continue

    # Sort primarily by category, then by order, then by title
    docs.sort(key=lambda d: (d.category, d.order, d.title))
    return docs


def get_subject_grouped_by_category(
    subject: str, vertical: Optional[str] = None
) -> Dict[str, List[DocumentMetadata]]:
    """Groups documents by their category for clean sidebar/hub rendering."""
    docs = list_documents_for_subject(subject, vertical)
    grouped: Dict[str, List[DocumentMetadata]] = {}
    for doc in docs:
        grouped.setdefault(doc.category, []).append(doc)
    return grouped


def get_subject_summary(subject: str) -> Optional[Dict[str, Any]]:
    """Returns subject details and vertical resource counts."""
    info = SUBJECTS.get(subject)
    if not info:
        return None

    docs = list_documents_for_subject(subject)
    vertical_counts: Dict[str, int] = {v: 0 for v in VERTICALS}
    for doc in docs:
        if doc.vertical in vertical_counts:
            vertical_counts[doc.vertical] += 1

    return {
        **info,
        "total_resources": len(docs),
        "counts": vertical_counts,
        "documents": docs,
    }


def get_all_subjects_summary() -> List[Dict[str, Any]]:
    """Returns overview list of all subjects with their resource counts."""
    summaries = []
    for slug in SUBJECTS:
        summary = get_subject_summary(slug)
        if summary:
            summaries.append(summary)
    return summaries
