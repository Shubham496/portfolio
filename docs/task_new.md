# MYTHOS ONLINE INSTITUTE — MASTER ROADMAP & TASK GUIDE (task_new.md)

> **CORE PURPOSE OF THE PLATFORM**:
> The site is a **lead machine for live cohorts**, not a shop for ₹10 items.
> Its job, in order: **Get found on Google &rarr; Build trust &rarr; Capture Name + WhatsApp number &rarr; Move people to a free demo class &rarr; Enroll them in a cohort.**
> Small bundle sales are a bonus, deferred to Phase 6.

---

## 1. Immutable Operational & Platform Rules

These rules are non-negotiable across all development phases:

1. **Strict Push Restriction (Platform Owner Only)**:
   * Only the platform owner is authorized to execute `git push` or deploy to production.
   * AI agents must test, stage, and commit locally with clean git status.
2. **Never Expose Secrets or Commit Ignored Assets**:
   * Never commit `.env`, passwords, tokens, API keys, or `*.db` files.
   * Large binary assets, datasets, and high-res media must stay in `external_assets/`.
3. **Zero Code Execution on Platform**:
   * All code blocks remain static syntax-highlighted reference elements. No interactive consoles or execution runners.
4. **Zero Public Cohort Pricing**:
   * Live cohort tuition is **never displayed** on public browse pages. Cohort admissions are handled through counseling and free demo classes.
   * A price may appear only at a future digital paywall or when someone explicitly clicks to buy.
5. **Contact Fields Invariant**:
   * **Full Name** and **WhatsApp/Phone** are mandatory on all student forms.
   * **Email is strictly optional** across all student-facing forms.
6. **Hidden Admin Portal**:
   * Admin routes have no public header or footer links.
   * Public administrative signup routes remain permanently disabled (redirecting to `/admin/login`).
7. **Two-Tier Navigation Architecture**:
   * Top navigation bar links exclusively between pages.
   * Universal left rail navigates sections within a page.
8. **No Invented Project Information or Fake Proof**:
   * Ground every technical statement in verified code.
   * Never fabricate names, numbers, credentials, or testimonials. Use a `[PLACEHOLDER]` token instead.

---

## 2. Owner-Approved Directives (Overriding Legacy Specs)

These directives supersede prior specifications in `GUIDE.md` and legacy roadmaps:

1. **Two Mentors (Clear Separation of Disciplines)**:
   * **Digital Marketing Mentor**: The owner's partner, displayed with real name, photo, bio, and LinkedIn link via `[DM_MENTOR_NAME]`, `[DM_MENTOR_PHOTO]`, `[DM_MENTOR_BIO]`, and `[DM_MENTOR_LINKEDIN]`.
   * **Data Analytics Mentor**: Strictly **anonymous** (no personal name, no photo), displayed as the *Mythos Data Analytics Mentor* with a grounded, neutral profile (3+ years teaching, 400+ learners taught, core tools covered).
   * **Discipline Isolation**: The Digital Marketing mentor is never represented as teaching Data Analytics, and the Data Analytics mentor is never represented as teaching Digital Marketing.
2. **One Subject at a Time (Data Analytics Track)**:
   * The Data Analytics cohort runs **one subject per batch** (~8 weeks per subject): SQL, Excel, Power BI, Python, Tableau, Git & GitHub.
   * The platform shows what subject is enrolling now and what comes next.
3. **Track-Specific Cohort Schedules**:
   * Data Analytics cohorts run **Saturday & Sunday, 6:00 PM – 8:00 PM IST**.
   * Digital Marketing cohorts run on `[DM_SCHEDULE]`. Schedules are batch-specific attributes, not hardcoded global singletons.
4. **Trust Claim Standardization**:
   * Expunge all mentions of *"550+ Students Trained"*.
   * Replace with `[TRUST_CLAIM]` (default: *"400+ learners taught by our mentors over 3+ years"*).
5. **Dynamic Contact & Communication Details**:
   * Business email and WhatsApp numbers must load from environment variables (`BUSINESS_EMAIL`, `BUSINESS_WHATSAPP`), never hardcoded.
   * Purge legacy hardcoded personal email (`shubhamsinghh057@gmail.com`) and phone (`8727864157`).

---

## 3. Placeholders Inventory (Owner-Supplied Data)

The following items are strictly provided by the platform owner. AI agents must use these exact bracketed identifiers until the owner provides verified production values:

* `[DM_MENTOR_NAME]`: Digital Marketing mentor's full name.
* `[DM_MENTOR_PHOTO]`: File path/URL for the DM mentor's professional photo.
* `[DM_MENTOR_BIO]`: Verified professional background and track record for DM mentor.
* `[DM_MENTOR_LINKEDIN]`: Verified LinkedIn profile URL for DM mentor.
* `[DM_SCHEDULE]`: Schedule timings for Digital Marketing cohorts.
* `[BUSINESS_EMAIL]`: Official institute business email address (env: `BUSINESS_EMAIL`).
* `[BUSINESS_WHATSAPP]`: Official institute WhatsApp contact number (env: `BUSINESS_WHATSAPP`).
* `[WHATSAPP_CHANNEL_URL]`: Public link to the Mythos WhatsApp community channel.
* `[TELEGRAM_URL]`: Link to the student Telegram group/channel.
* `[INSTAGRAM_URL]`: Official Mythos Instagram page.
* `[LINKEDIN_PAGE_URL]`: Official Mythos LinkedIn company/institute page.
* `[YOUTUBE_URL]`: Official Mythos YouTube channel.
* `[GOOGLE_SITE_VERIFICATION]`: Google Search Console site verification token.
* `[SUBJECT_ORDER]`: Curriculum sequence for Data Analytics (default: SQL, Excel, Power BI, Python, Tableau, Git and GitHub).
* `[DEMO_CLASS_DATETIME]`: Scheduled date, time, and meeting link for the upcoming free demo class.
* `[LEAD_MAGNET_FILES]`: Downloadable cheat sheets and practice datasets hosted in `external_assets/`.
* `[TRUST_CLAIM]`: Standardized credibility statement (default: *"400+ learners taught by our mentors over 3+ years"*).
* `[TESTIMONIALS]`: Real student reviews only. The testimonials UI component remains dormant/hidden until genuine submissions are supplied.

---

## 4. Completed Foundations & Existing Architecture

The following infrastructure has been implemented, tested, and verified clean:
* **FastAPI Core Engine**: Lightweight ASGI architecture running on Uvicorn with sub-100ms server-side rendering.
* **Component-Decomposed Jinja2 Templates**: Modular sections (`hero.html`, `programs.html`, `syllabus.html`, etc.).
* **Knowledge & Documentation Engine**: PyMdown markdown parsing, header anchor IDs, Table of Contents extraction, and LRU/TTL caching.
* **Sequential W3Schools-Style Study Tracks**: Complete curriculum topic trees for SQL and Python with `< Previous Topic` and `Next Topic >` navigation.
* **Dual-Engine Database Architecture**: SQLite for local zero-setup execution, PostgreSQL for cloud deployment.
* **Protected Instructor Admin Portal**: Session cookie authentication, leads pipeline management, and CSV export.
* **Automated Test Baseline**: 46 automated pytest test cases passing cleanly.

---

## 5. Master Implementation Roadmap (Phases 0 through 6)

Development is conducted **one phase at a time**. Each phase is verified, tested, documented, and locally committed before advancing.

```
Phase 0: Security & Privacy (DO FIRST)
  │
Phase 1: Be Findable (SEO & Quality Gate)
  │
Phase 2: Trust & People (Mentors, Contact Cleanup, 400+ Trust Claim)
  │
Phase 3: Cohort Display (One Subject at a Time, Roadmap Strip, Batch CRUD)
  │
Phase 4: Lead Capture & Funnel (Demo Class, Lead Magnets, UTMs, Anti-Spam)
  │
Phase 5: Analytics (Privacy-Friendly Events & Admin Funnel Card)
  │
Phase 6: Later Only (Optional Paywalled Bundles via External Link)
```

---

### Phase 0: Security & Privacy (COMPLETED)
*The platform is about to scale student contact capture; privacy and access boundaries are now fully hardened.*

* [x] **Task 0.1: Lock the Lead API Endpoints**
  * Verified authentication guards on all `/api/courses/leads*` and `/batches` creation endpoints.
  * Enforced `require_admin` on:
    * `GET /api/courses/leads`
    * `GET /api/courses/leads/summary`
    * `GET /api/courses/leads/export.csv`
    * `GET /api/courses/leads/{id}`
    * `PATCH /api/courses/leads/{id}/status`
    * `POST /api/courses/batches`
  * Confirmed that only public admissions actions stay unauthenticated: `POST /api/courses/enquiry`, `POST /api/courses/register`, `GET /api/courses/batches`, and `GET /api/courses/instructor`.
  * Added automated tests proving anonymous requests to lead endpoints return HTTP 401 Unauthorized.
* [x] **Task 0.2: Enforce SECRET_KEY Discipline**
  * Removed hardcoded default fallback secrets from `app/core/base_config.py`, `app/apps/courses/auth.py`, and documentation.
  * In production mode (`ENVIRONMENT=production` or `deployment`), raises an immediate startup error if `SECRET_KEY` is absent or set to an insecure placeholder.
  * Documented secret generation command (`python -c "import secrets; print(secrets.token_hex(32))"`).
* [x] **Task 0.3: Consent Capture & Legal Policy Pages**
  * Added policy pages with clear, plain-language placeholder text for owner review:
    * `/privacy` (`app/templates/legal/privacy.html`): Data collection, WhatsApp communication policy, zero data-selling guarantee.
    * `/terms` (`app/templates/legal/terms.html`): Terms of service, intellectual property, cohort enrollment guidelines.
    * `/refund-policy` (`app/templates/legal/refund_policy.html`): Clear refund and rescheduling policies.
  * Added a mandatory consent checkbox on all inquiry, registration, and lead capture forms:
    > *"I agree to be contacted by phone or WhatsApp about this course."*
  * Extended `StudentLead` database model and schemas to store:
    * `consent_given`: `Boolean`, default `True`.
    * `consent_at`: `DateTime`, timestamp of consent.
  * Added `do_not_contact` to allowed lead statuses so counselors can immediately suppress outreach if requested.
* [x] **Task 0.4: Log Redaction & Zero PII in Logs**
  * Audited all application loggers and added `mask_phone` and `mask_email` redaction utilities.
  * Ensured phone numbers, email addresses, and student names are never emitted in plaintext to standard output, file logs, or task logs. Sensitive tokens in logging statements are masked (`clean[:3] + "****" + clean[-2:]`).

---

### Phase 1: Be Findable (SEO & Quality Gate) (COMPLETED)
*Ensure search engines index high-quality content while excluding drafts and private surfaces.*

* [x] **Task 1.1: Dynamic Sitemap & Search Directives**
  * Implemented dynamic `GET /sitemap.xml` listing the home page, `/about`, `/demo`, `/register`, active subject hubs, datasets, and published notes with `<lastmod>` and `<changefreq>`. Excluded drafts.
  * Implemented dynamic `GET /robots.txt` disallowing `/admin/`, `/api/`, `/student/`, and pointing to `/sitemap.xml`.
* [x] **Task 1.2: Meta Tags, Open Graph & Canonical URLs**
  * Added unique `<title>`, `<meta name="description">`, `<link rel="canonical">`, and Open Graph (`og:title`, `og:description`, `og:image`, `og:url`) and Twitter Cards to every template.
  * Derived canonical URLs from `BASE_URL` loaded from environment (fallback: `https://mythostech.in`).
* [x] **Task 1.3: Google Search Console Verification Meta Tag**
  * Supported optional `GOOGLE_SITE_VERIFICATION` environment variable.
  * Injected `<meta name="google-site-verification" content="...">` in `app/templates/base.html` when configured.
* [x] **Task 1.4: Schema.org JSON-LD Structured Data**
  * Home page: `EducationalOrganization` schema with name, URL, logo, and social profile links; `Course` schemas for cohort tracks.
  * Technical Notes: `TechArticle` and `BreadcrumbList` schemas on hand-written, published documentation articles.
* [x] **Task 1.5: Content Quality Gate (Draft vs. Published Frontmatter)**
  * Added `status: "published" | "draft"` frontmatter attribute to documentation metadata.
  * Hand-authored articles are marked `published`.
  * Placeholder catalog topics synthesized from blueprints are treated as `draft`:
    * Injected with `<meta name="robots" content="noindex, nofollow">`.
    * Excluded from `sitemap.xml`.
    * Displayed in topic sidebars with a clean "Coming Soon" badge with no filler body.
  * Resource counters across the library display only published articles.
* [x] **Task 1.6: Web Performance & Static Asset Caching**
  * Configured HTTP cache-control headers on static assets (`max-age=31536000, immutable`).
  * Enabled `GZipMiddleware` on FastAPI application.
  * Added `loading="lazy"` on all template images.
  * Verified `GET /health` responds in <20ms for external uptime pingers.
* [x] **Task 1.7: Breadcrumb & Contextual Funnel Integration**
  * Included structured breadcrumb navigation on all library subpages.
  * Mounted contextual free demo-class CTA card on note and study track pages.

---

### Phase 2: Trust & People (Mentors & Brand Transparency) (COMPLETED)
*Transform the platform's human credibility with clear mentor separation and honest claims.*

* [x] **Task 2.1: Dual-Mentor Showcase & Dedicated `/about` Page**
  * Rebuilt the Mentorship section on the landing page (`app/templates/sections/mentor.html`) and dedicated `/about` page (`app/templates/about.html`):
    * **Digital Marketing Mentor**: Shows `[DM_MENTOR_NAME]`, professional photo container `[DM_MENTOR_PHOTO]`, verified bio `[DM_MENTOR_BIO]`, and LinkedIn `[DM_MENTOR_LINKEDIN]`.
    * **Data Analytics Mentor**: Shows as the *Mythos Data Analytics Mentor* (anonymous, no photo, high-tech emblem), with a grounded profile highlighting 3+ years teaching, 400+ learners taught, and practical tools covered.
    * Strict discipline separation: each mentor owns exclusively their subject domain.
* [x] **Task 2.2: Systematic Purge of the "550+" Metric**
  * Searched and replaced every occurrence of "550+" students across all HTML templates, static files, Python services, PDF generators, and test assertions.
  * Replaced with `[TRUST_CLAIM]` (default: *"400+ learners taught by our mentors over 3+ years"*).
* [x] **Task 2.3: Contact Information Migration & PDF Brochure Regeneration**
  * Moved all support and admissions contacts to `BUSINESS_EMAIL` and `BUSINESS_WHATSAPP` loaded from `app/core/base_config.py`.
  * Removed hardcoded `shubhamsinghh057@gmail.com` and `8727864157` from templates, footer, registration modals, syllabus generator, and documentation.
  * Re-rendered `app/static/pdf/Data_Analysis_Syllabus.pdf` reflecting new mentor credentials and dynamic contact information.
* [x] **Task 2.4: Dormant Testimonials Component**
  * Built a clean testimonials section partial (`app/templates/sections/testimonials.html`).
  * If no real testimonials exist in the database or config, the component renders nothing (completely hidden).
  * Never synthesizes placeholder reviews, quotes, or fake corporate logos.
* [x] **Task 2.5: Compliance & Guarantee Audit**
  * Audited all copy to eliminate any phrasing promising guaranteed jobs, placements, or specific salary figures.
  * Framed all outcomes around practical skill mastery, portfolio readiness, and interview preparation.

---

### Phase 3: Modular Cohort & Subject Display (COMPLETED)
*Structure cohort offerings so students see clear track specialization and enrollment progression.*

* [x] **Task 3.1: Track-Grouped Cohort Explorer**
  * Restructured cohort query and display (`app/templates/sections/programs.html` and `/register`):
    * Grouped by Track: **Data Analytics & BI Track** vs. **Digital Marketing Track**.
    * Grouped by Lifecycle: **Now Enrolling**, **Running**, and **Next in Queue**.
    * Past cohorts archived to a clean collapsed historical drawer.
* [x] **Task 3.2: Data Analytics Roadmap Strip & Next-Subject Waitlist**
  * Embedded horizontal curriculum roadmap strip for Data Analytics showing `[SUBJECT_ORDER]` (SQL &rarr; Excel &rarr; Power BI &rarr; Python &rarr; Tableau &rarr; Git/GitHub).
  * Visually highlighted the subject enrolling now with a badge: *"One subject per batch so you go deep."*
  * Added **"Notify Me for Next Batch"** button and modal creating a `waitlist` lead tied to the selected subject (`POST /api/courses/waitlist`).
* [x] **Task 3.3: Digital Marketing Track Schedule & Profile**
  * Rendered Digital Marketing cohorts with `[DM_SCHEDULE]` and mentor attribution linked to the DM mentor profile (`[DM_MENTOR_NAME]`, `/about#dm-mentor`).
  * Isolated Data Analytics cohorts to the anonymous *Mythos Data Analytics Mentor* (Sat & Sun 6–8 PM IST).
* [x] **Task 3.4: Admin Cohort & Batch Manager**
  * Added dedicated management panel in `/admin/batches` (`app/templates/admin/batches.html`) allowing the platform owner to:
    * Create, edit, and update batches (`batch_code`, `title`, `course_name`, `track`, `technologies`, `schedule_days`, `schedule_time`, `start_date`, `duration`, `max_seats`, `status`, `is_active`).
    * Close or archive batches without modifying application code.
* [x] **Task 3.5: Public Seat Scarcity Display**
  * Displayed available seats as an honest number calculated from remaining capacity (`remaining_seats = max_seats - total_registrations`).
  * Strictly zero tuition pricing on browse cards.

---

### Phase 4: Lead Capture, Demo Class & Funnel Optimization (COMPLETED)
*Streamline the visitor-to-student journey with frictionless demo registration and lead magnets.*

* [x] **Task 4.1: Database Schema Expansion for Funnels & Attribution**
  * Add lead types to `StudentLead`: `demo_class`, `waitlist`, `lead_magnet`, `enquiry`, `batch_registration`.
  * Add tracking columns to `StudentLead`:
    * `source_utm`: `String(255)` (concatenated or JSON of `utm_source`, `utm_medium`, `utm_campaign`).
    * `referrer_url`: `String(255)`.
    * `subject_interest`: `String(100)` (e.g., SQL, Power BI, Meta Ads).
    * `consent_given`: `Boolean`, default `True`.
    * `consent_at`: `DateTime`.
    * `follow_up_date`: `Date`, nullable.
  * Implement an idempotent startup migration checking and adding columns safely on SQLite and PostgreSQL.
* [x] **Task 4.2: Dedicated Free Demo Class Landing Page (`/demo`)**
  * Build dedicated route `GET /demo` (`app/templates/demo.html`):
    * Highlight date and time of next live demo session (`[DEMO_CLASS_DATETIME]`).
    * Simple high-converting form: Full Name, WhatsApp Number, optional Email, Subject Interest, and mandatory Consent Checkbox.
    * Confirmation screen with "Add to Google Calendar" button and link to join the WhatsApp Community Channel.
* [x] **Task 4.3: Free Lead Magnets (Cheat Sheets & Clean Datasets)**
  * Add contextual lead magnet callouts on subject hubs and note sidebars:
    * E.g., *"Download the Free SQL Interview Traps Cheat Sheet (PDF)"* or *"Download Indian E-Commerce 50k Dataset"*.
  * Short modal/form (Name, WhatsApp, Consent) reveals the direct download link upon submission.
  * Core notes remain 100% public with no login wall.
* [x] **Task 4.4: Community Channel Direct Action Links**
  * Add prominent join buttons for the official **WhatsApp Community Channel** (`[WHATSAPP_CHANNEL_URL]`) and **Telegram Group** (`[TELEGRAM_URL]`) in footer, confirmation pages, and note reading sidebars.
* [x] **Task 4.5: First-Touch UTM Capture & Cookie Persistence**
  * Implement lightweight middleware storing incoming `utm_source`, `utm_medium`, `utm_campaign`, and `ref` in a first-party cookie (`mythos_utm`, 30 days).
  * Automatically attach captured UTM metadata whenever a visitor submits an inquiry, demo request, or registration.
* [x] **Task 4.6: Admin Pipeline Management Overhaul**
  * Expand `/admin/dashboard` lead statuses: `new`, `contacted`, `demo_attended`, `enrolled`, `closed`, `do_not_contact`.
  * Add multi-filter controls by Lead Type, Traffic Source, and Subject Interest.
  * Add counselor follow-up date picker and notes updater.
  * Update CSV export to include UTM source, subject interest, and consent timestamp.
* [x] **Task 4.7: Anti-Spam & Rate Limiting**
  * Add invisible honeypot form fields (`website_url_hp`) on all public forms; reject submissions where the honeypot is filled.
  * Implement in-memory IP rate limiting on public submission endpoints to prevent automated spam abuse.

---

### Phase 5: Privacy-Friendly Analytics & Funnel Monitoring
*Monitor acquisition channels and conversion rates without tracking cookies.*

* [x] **Task 5.1: Privacy-Friendly Analytics Integration**
  * Support lightweight script injection via environment variable (`ANALYTICS_SCRIPT` for Plausible, Umami, or Cloudflare Web Analytics, or `GA4_MEASUREMENT_ID`).
  * Track custom client events: `cta_click`, `form_submit`, `lead_magnet_download`, `whatsapp_join` with automatic dispatch to Plausible, Umami, GA4, and the internal activity logging endpoint.
* [ ] **Task 5.2: Admin Funnel Summary Card**
  * Add an executive conversion metric card on `/admin/dashboard`:
    * Weekly leads by traffic source (WhatsApp, Google, Direct, Referral).
    * Total demo class registrants vs. attended.
    * Cohort enrollment conversion rate.

---

### Phase 6: Paywalls & Digital Bundles (LATER ONLY)
*To be implemented only after steady organic traffic and cohort counseling volume are established, upon explicit platform owner directive.*

* [ ] **Task 6.1: External Payment Link Integration**
  * Support optional external UPI/Razorpay payment link from environment variables.
  * Price is strictly shown only at the purchase gate (never on public browse surfaces).
  * No complex custom payment gateway or wallet integration until required.

---

## 6. Definition of Done

Every phase is considered done when:
1. **Automated Verification**: Full test suite passes cleanly (`python -m pytest -v`) with 0 failures, including new test cases for added features.
2. **Quality Gate**: Only hand-authored, published articles are indexable; draft topics display "Coming Soon" with noindex tags.
3. **Frictionless Funnel**: A visitor can register for a demo class or access a lead magnet in under 60 seconds.
4. **Data Integrity**: Leads appear in the admin pipeline with traffic source, subject interest, and consent timestamp.
5. **Brand Cleanliness**: Zero personal contact details, zero 550+ references, and zero unverified claims remain in code, templates, or tests.
6. **Git Hygiene**: Changes staged, clean local commit created with conventional message, and zero untracked scratch files remaining. **NO `git push`**.
