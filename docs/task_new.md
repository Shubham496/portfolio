# ARCHITECTURAL ROADMAP & TASK GUIDE: MYTHOS KNOWLEDGE & RESOURCE ENGINE

## 1. Mission, Strategic Intent & Micro-Monetization Model

### 1.1 Primary Objective
Transform `mythostech.in` from a pure cohort landing page into an **authoritative educational repository, dataset vault, and practice hub** for Indian college students (B.Tech, BCA, MCA, BSc IT) and junior developers.

### 1.2 The Problem We Solve
College curricula and superficial online tutorials teach outdated theory and half-truths (e.g., teaching that SQL joins only happen on PK/FK using `=` equality, omitting non-equi joins, execution planners, and `NULL` traps). 
Mythos bridges the gap: giving students the exact structured answers they need to **score top marks in university exams and vivas**, while equipping them with **real production depth** to pass technical interviews.

---

### 1.3 Monetization Ladder & Micro-Pricing Strategy

To maximize mass distribution across Indian university networks, we adopt a **Micro-Transaction Funnel**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: 100% PUBLIC & FREE (NO LOGIN REQUIRED)                         │
│ • Core Academic & Production Notes (SQL, Python, BI, SEO)              │
│ • Preview Questions (Top 10-15 Viva & Interview gotchas)               │
│ • Mini Data Snippets (for follow-along tutorials)                      │
│ Strategy: Instant zero-friction access, WhatsApp/Telegram virality,    │
│           and maximum Google SEO indexing.                             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Unlocks downloads & saved progress
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 2: FREE REGISTERED STUDENT ACCOUNT (LOGIN REQUIRED)               │
│ • Free Complete Datasets (.csv, .xlsx, .sqlite with data dictionaries) │
│ • Reading progress tracking and bookmarking                            │
│ • Access to community discussion / feedback                            │
│ Strategy: Captures high-intent leads (Name, WhatsApp, Email, College). │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Instant UPI micro-purchases
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 3: MICRO-TRANSACTIONS (MASS STUDENT ADOPTION: ₹10 – ₹49)          │
│ • Full Solved Viva & Interview Question Banks: ₹10                     │
│ • Complete Semester Exam Notes Bundles: ₹20 – ₹29                      │
│ • Quick Revision / Lab Manual Kits: ₹29 – ₹49                          │
│ Strategy: Pocket-money impulse buys (cheaper than a chai/snack).       │
│           Converts free readers into paying, verified customers via    │
│           frictionless 1-click UPI payments.                           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Premium digital products & cohorts
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 4: PREMIUM DIGITAL PRODUCTS & HIGH-TICKET COHORTS                 │
│ • Full Books & Comprehensive Handbooks: ₹99 – ₹199                     │
│ • End-to-End Downloadable Capstone Projects (code + data + docs): ₹149 │
│ • MYTHOS Live Weekend Cohorts (Live Mentorship with Shubham Singh):    │
│   - Tuition pricing is NEVER displayed online (remains pure admissions │
│     orientation & counseling model via /register).                     │
│   - Organic readers of notes & books convert directly to cohort leads. │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Platform Information Architecture & Content Verticals

Content is organized under **5 distinct verticals**, accessible via a unified **Resource Hub** (`/library`):

```
                   ┌─────────────────────────────────────────┐
                   │             MYTHOS LIBRARY              │
                   └─────────────────────────────────────────┘
                                        │
         ┌──────────────┬───────────────┼───────────────┬──────────────┐
         ▼              ▼               ▼               ▼              ▼
     [Notes]       [Practice/Viva]  [Datasets]       [Books]       [Projects]
    Deep theory    Oral exam Q&A,   Clean real-world Comprehensive Full source code,
    vs. production lab codes, and   CSVs/databases   eBooks and    clean data, and
    gotchas        interview prep   for portfolios   handbooks     case studies
```

### 2.1 The Unified Subject Hub (`/library/{subject}`)
When a student selects a subject (e.g., `SQL`, `Python`, `PowerBI`, `Digital Marketing`), they land on a unified dashboard with intuitive resource tabs:
* `[ 📝 Notes (15) ]`: Structured chapters from fundamentals to production internals.
* `[ 🎯 Practice & Viva (45) ]`: University lab viva questions + junior interview traps.
* `[ 📊 Datasets (6) ]`: Clean, ready-to-query practice datasets with sample business questions.
* `[ 📚 Books & Guides (2) ]`: Downloadable PDF guides and comprehensive handbooks.
* `[ 🚀 Capstone Projects (3) ]`: Real-world end-to-end portfolio projects.

---

## 3. User Experience & UI Architecture

### 3.1 Design Philosophy: Modern Technical Documentation Engine
* **Lightweight Server-Side Rendering (SSR)**: Built natively with FastAPI + Jinja2 for sub-100ms TTFB on Render.io free tier. No heavy frontend SPA frameworks.
* **Three-Column Reading Layout**:
  1. **Left Navigation Tree**: Collapsible categories, topics, and chapters with completion indicators.
  2. **Center Reading Canvas**: Wide, distraction-free typography using Mythos Poppins/Inter design tokens, copyable syntax-highlighted code blocks (Prism.js via CDN), and styled callout boxes (`> [!NOTE]`, `> [!EXAM]`, `> [!PRO-TIP]`).
  3. **Right Sticky Sidebar**: On-page Table of Contents (TOC) + Contextual Cohort/Resource CTA card.
* **Social Sharing Bar**: Sticky one-click "Share to WhatsApp Class Group" and "Share to Telegram" buttons on every note and viva set.
* **Mobile Experience**: Clean off-canvas slide-out drawer for navigation and responsive typography.

---

## 4. Database Architecture & Customer Activity Tracking

### 4.1 Access Control Matrix
| Resource | Public / Guest | Free Registered Student | Paid Micro-Purchase (₹10-₹49) | Paid Book / Project |
| :--- | :---: | :---: | :---: | :---: |
| Public Notes & Articles | ✅ Full Access | ✅ Full Access | ✅ Full Access | ✅ Full Access |
| Preview Questions (Top 10) | ✅ Full Access | ✅ Full Access | ✅ Full Access | ✅ Full Access |
| Full Viva/Interview Bank | ❌ Preview Only | ❌ Preview Only | ✅ Unlocked (₹10) | ✅ Full Access |
| Basic Sample Data Snippets | ✅ View Online | ✅ View Online | ✅ View Online | ✅ View Online |
| Full Downloadable Datasets | ❌ Locked | ✅ Instant Download | ✅ Instant Download | ✅ Instant Download |
| Bookmark & Reading Progress | ❌ | ✅ Active | ✅ Active | ✅ Active |
| Books & Capstone Projects | ❌ | ❌ | ❌ | ✅ Unlocked (₹99+) |

---

### 4.2 Data Models Specification

```
                ┌──────────────────┐
                │      users       │
                └────────┬─────────┘
                         │ 1:N
         ┌───────────────┼───────────────┐
         ▼                               ▼
┌──────────────────┐           ┌──────────────────┐
│user_activity_logs│           │  user_purchases  │
└──────────────────┘           └────────┬─────────┘
                                        │ N:1
                               ┌────────▼─────────┐
                               │ digital_products │
                               └──────────────────┘
```

#### 1. `users` Table
* `id`: `Integer`, Primary Key, Autoincrement.
* `full_name`: `String(120)`, Not Null.
* `phone`: `String(30)`, Unique, Indexed, Not Null (WhatsApp number for cohort counseling).
* `email`: `String(150)`, Unique, Indexed, Nullable.
* `hashed_password`: `String(255)`, Not Null.
* `user_type`: `String(50)`, Default `"student"` (`"student"`, `"fresher"`, `"working_professional"`).
* `college_or_company`: `String(150)`, Nullable.
* `is_active`: `Boolean`, Default `True`.
* `created_at`: `DateTime`, Default `utcnow`.

#### 2. `user_activity_logs` Table (Behavior & Analytics Engine)
Tracks engagement to inform future content decisions and identify high-intent cohort prospects:
* `id`: `Integer`, Primary Key, Autoincrement.
* `user_id`: `Integer`, FK -> `users.id`, Nullable (tracks both guest sessions and logged-in users).
* `session_id`: `String(64)`, Indexed (cookie-based session ID linking guest behavior before login).
* `event_type`: `String(50)`, Indexed (`page_view`, `note_read`, `dataset_download`, `question_unlocked`, `purchase_click`, `cohort_apply_click`).
* `resource_type`: `String(50)` (`note`, `viva`, `dataset`, `book`, `project`).
* `resource_slug`: `String(100)`, Indexed.
* `referrer`: `String(255)`, Nullable (e.g., `whatsapp`, `telegram`, `google`).
* `ip_address`: `String(50)`, Nullable.
* `created_at`: `DateTime`, Default `utcnow`, Indexed.

#### 3. `digital_products` Table
* `id`: `Integer`, Primary Key, Autoincrement.
* `slug`: `String(100)`, Unique, Indexed.
* `title`: `String(200)`, Not Null.
* `product_type`: `String(50)` (`viva_bank`, `notes_bundle`, `book`, `capstone_project`).
* `price_inr`: `Integer`, Not Null (e.g., `10`, `20`, `99`, `149`).
* `file_asset_url`: `String(255)`, Nullable (secure external CDN / Cloud storage download link).
* `is_active`: `Boolean`, Default `True`.

#### 4. `user_purchases` Table
* `id`: `Integer`, Primary Key, Autoincrement.
* `user_id`: `Integer`, FK -> `users.id`, Indexed.
* `product_id`: `Integer`, FK -> `digital_products.id`, Indexed.
* `amount_paid`: `Integer`, Not Null.
* `payment_provider`: `String(50)`, Default `"razorpay"` / `"cashfree"`.
* `transaction_ref`: `String(150)`, Unique, Indexed.
* `status`: `String(50)`, Default `"completed"` (`pending`, `completed`, `failed`).
* `created_at`: `DateTime`, Default `utcnow`.

---

## 5. Architectural Constraints & Non-Negotiables

1. **Render.io Free-Tier Discipline (Zero Asset Bloat)**:
   * **No raw image assets, heavy PDFs, or massive datasets** committed to the core web repository.
   * Dataset files (`.csv`, `.zip`) and product PDFs must be hosted on decoupled cloud storage (e.g., Cloudflare R2, AWS S3, or GitHub Releases/jsDelivr) and served via signed or redirect URLs.
2. **Immutable Course Pricing Rule**:
   * **Live cohort tuition fees are NEVER listed on the website**.
   * Digital micro-products (₹10 viva sets, ₹20 notes, ₹99 books) have transparent, friction-free pricing with instant UPI checkout.
3. **Strict Git Discipline & Production Authority**:
   * Only the platform owner executes `git push` to `origin/main` or deploys to production.
   * AI agents must verify test suites (`python -m pytest -v`), stage all changes, and create clean local commits.

---

## 6. Phased Implementation Roadmap (Granular Task Breakdown)

### Phase 1: Core Library Engine, Base Routing & Technical Docs UI (Completed)
* [x] **Task 1.1: Dependency Specification**
  * Add `markdown>=3.6.0`, `python-frontmatter>=1.1.0`, and `pymdown-extensions>=10.7` to `requirements.txt`.
  * Ensure consistent dependencies across local development and Render.io production blueprints.
* [x] **Task 1.2: Content Discovery, Frontmatter Parsing & Caching Engine (`app/apps/library/services.py`)**
  * Implement frontmatter extraction (validates `title`, `slug`, `subject`, `vertical`, `category`, `order`, `tier`, `price_inr`, `reading_time`, `description`, `tags`).
  * Implement Markdown-to-HTML parser with `pymdownx` extensions: fenced code, syntax highlighting classes, tables, admonitions/callouts (`> [!NOTE]`, `> [!EXAM]`, `> [!PRO-TIP]`), and header anchor IDs.
  * Implement hierarchical Table of Contents (TOC) extractor parsing `<h2>` and `<h3>` tags with anchor links.
  * Implement filesystem content indexer scanning `app/content/{subject}/*.md` with category grouping and order sorting.
  * Implement in-memory TTL/LRU caching layer so parsed HTML and TOC are cached for fast (<50ms) retrieval on Render.io.
* [x] **Task 1.3: Library Web Routing (`app/apps/library/router.py`) & Application Mounting**
  * Create `app/apps/library/__init__.py` and `app/apps/library/router.py`.
  * Route 1: `GET /library` → Main Resource Hub (featured topics, subject cards, resource counts).
  * Route 2: `GET /library/{subject}` → Subject portal with vertical filter tabs (`notes`, `viva`, `datasets`, `books`, `projects`).
  * Route 3: `GET /library/{subject}/notes/{slug}` → 3-column technical docs reader view.
  * Handle edge cases: 404 for unknown subjects or invalid slugs with friendly fallback templates.
  * Mount router into `app/main.py`.
* [x] **Task 1.4: Documentation UI Templates (`app/templates/library/`)**
  * `app/templates/library/index.html`: Resource hub landing page showing subject cards (SQL, Python, Business Intelligence, Digital Marketing) with icon badges and resource count pills.
  * `app/templates/library/subject_hub.html`: Subject dashboard featuring vertical filter tabs, search/filter, and cards for Notes, Viva Banks, Datasets, and Handbooks.
  * `app/templates/library/reader.html`: 3-column technical docs reader:
    * Left Sidebar: Collapsible subject tree with active article highlight.
    * Center Canvas: Clean Poppins/Inter typography, Prism.js code blocks with "Copy Code" button, responsive tables, and styled callout boxes.
    * Right Sidebar: Sticky Table of Contents (TOC) with scroll spy and contextual Cohort CTA card.
    * Social Share Bar: WhatsApp ("Share with Class Group") and Telegram 1-click share buttons.
* [x] **Task 1.5: Navigation & Header Integration**
  * Update `app/templates/partials/navbar.html`: Add "Library" link in desktop & mobile menus.
  * Update `app/templates/partials/footer.html`: Add Resource Library links under quick resources.
* [x] **Task 1.6: Flagship Seed Article & Comprehensive Test Suite**
  * Author starter flagship note `app/content/sql/sql-joins-textbook-vs-reality.md` strictly following the 5-part blueprint.
  * Write `tests/test_library.py` verifying:
    * `/library` renders 200 with subject listings.
    * `/library/sql` renders 200 with tabs.
    * `/library/sql/notes/sql-joins-textbook-vs-reality` renders 200 with TOC, rendered code blocks, and frontmatter metadata.
    * Invalid subject or slug returns 404.
    * Caching correctly prevents redundant disk reads.
  * Verify full test suite passes (all 15 existing tests + new library tests).
  * Run local git status check, stage, and commit with descriptive commit message.

---

### Phase 1.5: Site-Wide Navigation Architecture, Zero-Upfront Pricing & Minimalist Icon Library Hub (Completed)
* [x] **Task 1.5.1: Top Navigation Bar Redesign (Inter-Page Links & Hover Menus)**
  * Restructure `app/templates/partials/navbar.html` so top navigation exclusively links to distinct pages:
    * **Courses & Cohorts**: Hover dropdown with links to Track 1 (Performance Marketing), Track 2 (SEO & Growth), and Track 3 (Data Analytics & BI).
    * **Notes & Handbooks**: Hover dropdown with links to `/library/sql?vertical=notes`, `/library/python?vertical=notes`, `/library/bi?vertical=notes`, and `/library/digital-marketing?vertical=notes`.
    * **Interview & Viva Questions**: Direct link to `/library?vertical=viva` or subject viva banks.
    * **Practice Datasets**: Direct link to `/library?vertical=datasets`.
    * **Admissions**: Dedicated link to `/register`.
  * Update mobile slide-out menu with matching multi-page navigation and accordion groups.
* [x] **Task 1.5.2: Universal Left-Side In-Page Section Navigator**
  * Implement standard left-side in-page navigation rail/dock with active scroll-spy:
    * On the landing page (`/`): Floating left dock allowing 1-click jumping between `#programs`, `#syllabus`, `#projects`, `#methodology`, `#career`, and `#about`.
    * On the documentation reader (`reader.html`): Preserved left chapter tree with active chapter indicator.
    * Include smooth scroll, tooltips, and responsive layout handling (collapsible on mobile/tablet).
* [x] **Task 1.5.3: Strict Zero-Upfront Pricing Audit & Enforcement**
  * Purge all upfront price figures ("₹10", "₹20", "₹99", "₹149", etc.) across all browse surfaces, card badges, header chips, and reader sidebars.
  * Replace with clear access status pills: "Free Guide", "Viva Bank", "Clean Dataset", "Capstone Repo".
  * Guarantee that prices are ONLY displayed when a student reaches a gated/locked asset or clicks to unlock/purchase.
* [x] **Task 1.5.4: Minimalist Icon-First Library Hub (`app/templates/library/index.html`)**
  * Completely redesign `/library` to eliminate textual clutter and long paragraphs.
  * Implement an uncluttered, high-impact grid of technology tiles displaying prominent official logos (MySQL, PostgreSQL, Python, Pandas, Power BI, Tableau, Excel, Google Ads/GA4, Meta Ads, SEO) and clean titles.
  * Direct 1-click routing to the technology's resources.
* [x] **Task 1.5.5: Non-Negotiable Enforcement: Strictly Zero Code Execution**
  * Verify that all code blocks remain static copy-only syntax elements with zero execution runners or interactive consoles.
* [x] **Task 1.5.6: Verification, Automated Tests & Git Hygiene**
  * Update test cases to reflect new navigation links and zero-upfront pricing.
  * Verify full test suite passes with 0 failures.
  * Stage and commit locally.

---

### Phase 2: Student Authentication, Access Control & Activity Logging
* [ ] **Task 2.1: Student User & Activity Logging Database Models**
  * Implement `users` model in `app/apps/courses/models.py` (or `app/apps/users/models.py`) with `phone` (mandatory/unique), `full_name` (mandatory), `email` (optional), `hashed_password`, `user_type`, and `college_or_company`.
  * Implement `user_activity_logs` model tracking `user_id`, `session_id`, `event_type`, `resource_type`, `resource_slug`, `referrer`, `ip_address`, and timestamp.
  * Run database migration / table initialization.
* [ ] **Task 2.2: Student Session Authentication**
  * Implement `GET /student/login`, `POST /student/login`.
  * Implement `GET /student/register`, `POST /student/register` (Phone/WhatsApp mandatory, email optional).
  * Implement `GET /student/logout`.
  * Signed HTTP-only cookie session management (`student_session`).
* [ ] **Task 2.3: Engagement Tracking & Activity Logger Service**
  * Implement lightweight logging helper to record `page_view`, `note_read`, `cohort_apply_click`, and `dataset_download_click`.
  * Track guest sessions via signed anonymous cookie UUID and link upon student login.
* [ ] **Task 2.4: Free Dataset Gating & Access Control**
  * Implement preview vs full download logic for datasets:
    * Guest users: Preview schema, sample top 10 rows, "Login to Download Full Dataset" CTA.
    * Authenticated students: One-click instant direct download link.

---

### Phase 3: Flagship Launch Content (High-Value Ingestion)
* [ ] **Task 3.1: Complete SQL Masterclass Note (Free Tier)**
  * Finalize `app/content/sql/sql-joins-textbook-vs-reality.md` with complete diagrams, non-equi joins, planner hash vs merge joins, and interview traps.
* [ ] **Task 3.2: SQL Viva & Interview Bank (Preview Free + ₹10 Unlock Gate)**
  * Author `app/content/sql/viva-top-45-interview-traps.md` with 45 solved questions.
  * Configure frontmatter `tier: "paid_micro"`, `price_inr: 10`.
  * Show questions 1–10 free; gate questions 11–45 behind ₹10 unlock prompt.
* [ ] **Task 3.3: Production Dataset 1 (Indian E-Commerce Orders)**
  * Create `datasets/indian_ecommerce_50k_orders.csv` in `external_assets/` and sync with CDN/GitHub Raw.
  * Author metadata document `app/content/sql/dataset-indian-ecommerce.md` with data dictionary, ER diagram, and 10 real-world business analytics challenge queries.
* [ ] **Task 3.4: Python Foundation Masterclass Note (Free Tier)**
  * Author `app/content/python/python-memory-and-mutable-traps.md` exploring mutable default arguments, `id()`, shallow vs deep copy, and interview gotchas.

---

### Phase 4: UPI Micro-Purchases & Checkout Pipeline
* [ ] **Task 4.1: Digital Products & Purchases Database Models**
  * Implement `digital_products` and `user_purchases` tables.
  * Seed initial products: SQL Viva Bank (₹10), SQL Notes Bundle (₹20), Full Handbook (₹99).
* [ ] **Task 4.2: UPI Payment Gateway Integration (Razorpay / Cashfree)**
  * Implement checkout initialization route `POST /api/library/purchase/initiate`.
  * Implement UPI QR modal and mobile UPI intent link (Google Pay, PhonePe, Paytm).
  * Implement webhook / verification endpoint `POST /api/library/purchase/verify`.
* [ ] **Task 4.3: Instant Digital Unlock & Delivery Experience**
  * Implement instant access grant: upon successful payment, unlock content and display confirmation receipt.
  * Provide downloadable asset link and email receipt if email was provided.

---

### Phase 5: Cohort Funnel Attribution & SEO Automation
* [ ] **Task 5.1: Contextual Cohort Callout Partials & UTM Attribution**
  * Build `app/templates/library/partials/cohort_card.html` with dynamic topic-aware copy (e.g. on SQL articles: "Ready to master SQL & Database Engineering live?").
  * Link directly to `/register?source=library_{subject}_{slug}` with prefilled track selection.
* [ ] **Task 5.2: Dynamic Sitemap Generation (`/sitemap.xml`)**
  * Build dynamic `GET /sitemap.xml` listing all landing pages, library hub, subject hubs, notes, viva banks, and datasets with `<lastmod>` and `<changefreq>`.
* [ ] **Task 5.3: Rich SEO Metadata & JSON-LD Structured Data**
  * Inject `TechArticle` schema into note reader pages.
  * Inject `FAQPage` schema into viva bank pages.
  * Inject `Dataset` schema into dataset pages for Google Dataset Search discovery.

---

## 7. Standard 5-Part Content Blueprint (For Every Note)

Whenever a note or guide is authored for the Mythos Library, it must follow this exact structure:

1. **Academic Definition & Core Concept:** Rigorous, textbook-clean explanation suitable for scoring full marks in a university written exam.
2. **Interactive Code & Query Examples:** Self-contained, copyable, syntax-highlighted examples with expected outputs.
3. **The Production Reality ("What Textbooks Skip"):** Real-world edge cases, performance implications, memory/disk trade-offs, and how senior engineers handle it.
4. **Exam & Interview Gotchas:** 3–5 high-frequency tricky questions examiners and interviewers ask to catch students off guard.
5. **Mythos Mentorship Bridge:** A one-sentence contextual bridge inviting readers to apply for the live hands-on Weekend Cohort.
