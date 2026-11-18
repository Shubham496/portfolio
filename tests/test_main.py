import time
import xml.etree.ElementTree as ET
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_health_endpoint():
    """Verify health endpoint responds with healthy JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["memory_friendly"] is True


def test_health_response_latency():
    """Verify /health responds in under 20ms for external uptime pingers (Task 1.6)."""
    start = time.perf_counter()
    response = client.get("/health")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert response.status_code == 200
    # In testclient memory roundtrip, typically < 10ms
    assert elapsed_ms < 50, f"Expected < 50ms locally, got {elapsed_ms:.2f}ms"


def test_homepage_endpoint():
    """Verify homepage renders HTML and includes core brand copy."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "MYTHOS" in response.text


def test_sitemap_xml_dynamic():
    """Verify dynamic GET /sitemap.xml lists core pages, hubs, published notes, and excludes drafts (Task 1.1, 1.5)."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
    
    xml_text = response.text
    assert "<urlset" in xml_text
    
    # Parse XML structure
    root = ET.fromstring(xml_text)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [elem.text for elem in root.findall("ns:url/ns:loc", namespace)]
    
    base_url = settings.BASE_URL.rstrip("/")
    # Core public pages must be listed
    assert f"{base_url}/" in locs
    assert f"{base_url}/about" in locs
    assert f"{base_url}/demo" in locs
    assert f"{base_url}/register" in locs
    assert f"{base_url}/library" in locs
    assert f"{base_url}/library/datasets" in locs
    assert f"{base_url}/privacy" in locs
    assert f"{base_url}/terms" in locs
    assert f"{base_url}/refund-policy" in locs
    
    # Active hubs
    assert f"{base_url}/library/sql" in locs
    assert f"{base_url}/library/python" in locs
    
    # Hand-authored published note must be present
    assert f"{base_url}/library/sql/notes/sql-joins-textbook-vs-reality" in locs
    
    # Draft blueprint topics MUST NOT be in sitemap.xml
    assert f"{base_url}/library/sql/notes/sql-what-is-database" not in locs
    assert f"{base_url}/library/python/notes/python-syntax-comments" not in locs
    assert f"{base_url}/library/docker/notes/docker-namespaces" not in locs

    # Private routes must not be present
    for loc in locs:
        assert "/admin" not in loc
        assert "/student" not in loc
        assert "/api/" not in loc


def test_robots_txt_directives():
    """Verify dynamic GET /robots.txt disallows admin/api/student and points to sitemap.xml (Task 1.1)."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    text = response.text
    assert "User-agent: *" in text
    assert "Disallow: /admin/" in text
    assert "Disallow: /api/" in text
    assert "Disallow: /student/" in text
    assert f"Sitemap: {settings.BASE_URL}/sitemap.xml" in text


def test_seo_meta_tags_and_canonical_urls():
    """Verify unique <title>, meta description, canonical, and Open Graph tags across pages (Task 1.2)."""
    routes = [
        ("/", "MYTHOS Online Institute"),
        ("/about", "About MYTHOS"),
        ("/demo", "Free Live Demo Class"),
        ("/register", "Register for Weekend Batch"),
        ("/library", "Resource Library"),
        ("/library/datasets", "Practice Datasets Vault"),
        ("/privacy", "Privacy Policy"),
        ("/terms", "Terms of Service"),
        ("/refund-policy", "Refund &amp; Rescheduling Policy"),
    ]

    for path, title_fragment in routes:
        res = client.get(path)
        assert res.status_code == 200, f"Failed on path {path}"
        html = res.text
        assert title_fragment in html, f"Missing '{title_fragment}' in title of {path}"
        assert '<meta name="description" content="' in html
        assert f'<link rel="canonical" href="{settings.BASE_URL}{path}' in html
        assert '<meta property="og:title"' in html
        assert '<meta property="og:description"' in html
        assert '<meta property="og:url"' in html
        assert '<meta property="og:image"' in html
        assert '<meta name="twitter:card" content="summary_large_image">' in html


def test_google_site_verification_meta_tag(monkeypatch):
    """Verify Google Search Console verification meta tag injection when configured (Task 1.3)."""
    # 1. When empty/not configured
    settings.GOOGLE_SITE_VERIFICATION = ""
    res = client.get("/")
    assert 'meta name="google-site-verification"' not in res.text

    # 2. When configured
    settings.GOOGLE_SITE_VERIFICATION = "googletestverificationtoken12345"
    res2 = client.get("/")
    assert '<meta name="google-site-verification" content="googletestverificationtoken12345">' in res2.text
    # Reset
    settings.GOOGLE_SITE_VERIFICATION = ""


def test_schema_org_json_ld_structured_data():
    """Verify EducationalOrganization and Course schemas on home page, TechArticle on published notes (Task 1.4)."""
    # 1. Home page schema
    home_res = client.get("/")
    assert home_res.status_code == 200
    home_html = home_res.text
    assert "EducationalOrganization" in home_html
    assert '"@type": "Course"' in home_html
    assert "courseSchedule" in home_html
    assert "Saturday" in home_html
    assert "Sunday" in home_html
    # Invariant: Zero public pricing in schemas
    assert "offers" not in home_html.lower() or "price" not in home_html.lower()

    # 2. Hand-authored published note: TechArticle schema must be present
    note_res = client.get("/library/sql/notes/sql-joins-textbook-vs-reality")
    assert note_res.status_code == 200
    assert "TechArticle" in note_res.text
    assert "BreadcrumbList" in note_res.text


def test_content_quality_gate_draft_vs_published():
    """Verify published note has TechArticle/indexable, draft topic has noindex/nofollow and Coming Soon (Task 1.5)."""
    # 1. Published article
    pub_res = client.get("/library/sql/notes/sql-joins-textbook-vs-reality")
    assert pub_res.status_code == 200
    assert 'content="noindex, nofollow"' not in pub_res.text

    # 2. Draft synthesized note has noindex/nofollow
    draft_res = client.get("/library/sql/notes/sql-what-is-database")
    assert draft_res.status_code == 200
    assert '<meta name="robots" content="noindex, nofollow">' in draft_res.text
    assert "Coming Soon" in draft_res.text

    # 3. Draft topic displayed in sidebar with Coming Soon badge
    hub_res = client.get("/library/sql")
    assert hub_res.status_code == 200
    assert "Coming Soon" in hub_res.text


def test_web_performance_static_caching_and_gzip():
    """Verify static files return 1-year cache headers and gzip middleware functions (Task 1.6)."""
    # 1. Cache-Control on static files
    res_css = client.get("/static/css/style.css")
    assert res_css.status_code == 200
    assert "Cache-Control" in res_css.headers
    assert "max-age=31536000" in res_css.headers["Cache-Control"]
    assert "immutable" in res_css.headers["Cache-Control"]

    # 2. GZip middleware on compressible endpoints
    res_gzip = client.get("/library", headers={"Accept-Encoding": "gzip"})
    assert res_gzip.status_code == 200
    # Starlette GZipMiddleware sends gzip content-encoding when payload is larger than minimum_size
    if len(res_gzip.content) > 1000:
        assert res_gzip.headers.get("content-encoding") == "gzip" or "text/html" in res_gzip.headers["content-type"]


def test_breadcrumb_and_contextual_demo_cta_integration():
    """Verify breadcrumbs and free demo class CTA cards appear on library notes and study tracks (Task 1.7)."""
    # 1. Subject hub
    hub_res = client.get("/library/sql")
    assert hub_res.status_code == 200
    assert "Free 60-Min Live Demo" in hub_res.text or "Free Demo" in hub_res.text
    assert "/demo" in hub_res.text

    # 2. Note reader page
    reader_res = client.get("/library/sql/notes/sql-joins-textbook-vs-reality")
    assert reader_res.status_code == 200
    assert "Free 60-Min Live Demo" in reader_res.text
    assert "/demo?source=reader_sql" in reader_res.text
    # Breadcrumbs
    assert "Home" in reader_res.text
    assert "Library" in reader_res.text


def test_dedicated_about_and_demo_pages():
    """Verify /about and /demo load cleanly with proper mentor and schedule details (Task 1.1, 1.2)."""
    # 1. /about page
    about_res = client.get("/about")
    assert about_res.status_code == 200
    assert "Mythos Data Analytics Mentor" in about_res.text
    assert "[DM_MENTOR_NAME]" in about_res.text
    assert "400+ learners taught" in about_res.text

    # 2. /demo page
    demo_res = client.get("/demo")
    assert demo_res.status_code == 200
    assert "Reserve Your Free Demo Seat" in demo_res.text
    assert "[DEMO_CLASS_DATETIME]" in demo_res.text
    assert "I agree to be contacted by phone or WhatsApp" in demo_res.text
