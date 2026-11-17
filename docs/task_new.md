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

## 6. Phased Implementation Roadmap

### Phase 1: Core Library Engine, Base Routing & Technical Docs UI
* [ ] **Task 1.1**: Add lightweight Markdown parsing dependencies (`markdown`, `python-frontmatter`, `pymdown-extensions`) to `requirements.txt`.
* [ ] **Task 1.2**: Implement `app/apps/library/` module:
  * `GET /library` → Main Resource Hub (featured topics, top datasets, popular notes).
  * `GET /library/{subject}` → Subject hub with tabs (`Notes`, `Practice`, `Datasets`, `Books`, `Projects`).
  * `GET /library/{subject}/notes/{slug}` → Technical docs reader view.
* [ ] **Task 1.3**: Build high-performance in-memory caching (LRU / TTL) for parsed markdown files.
* [ ] **Task 1.4**: Design Jinja2 templates extending `base.html`:
  * `app/templates/library/reader.html`: Clean 3-column technical documentation layout with Prism.js CDN code highlighting, copy button, sticky TOC, and WhatsApp/Telegram share buttons.
  * `app/templates/library/subject_hub.html`: Subject overview and tabbed resource explorer.
* [ ] **Task 1.5**: Update `app/templates/partials/navbar.html` to include the **Library** / **Resources** navigation menu.

### Phase 2: Student Authentication, Access Control & Activity Logging
* [ ] **Task 2.1**: Implement `users` and `user_activity_logs` models and migrations in `app/apps/courses/models.py` or new `app/apps/users/` module.
* [ ] **Task 2.2**: Implement student auth routes:
  * `GET /student/login`, `POST /student/login`
  * `GET /student/register`, `POST /student/register` (Phone/WhatsApp required, Email optional)
  * Session-based authentication via signed cookies.
* [ ] **Task 2.3**: Implement background / lightweight activity logging middleware or service to record page views, reading depth, and CTA interactions into `user_activity_logs`.
* [ ] **Task 2.4**: Implement dataset download gating: guest users see sample preview; logged-in users get instant one-click download.

### Phase 3: Flagship Launch Content (High-Value Ingestion)
* [ ] **Task 3.1: SQL Masterclass Note (Free)**:
  * *Title:* "SQL Joins: What Textbooks Teach vs. How Production Databases Actually Work"
  * *Covers:* Non-equi joins (`BETWEEN`, `<`, `>`), expression joins, `NULL` equality fallacy, and planner execution strategies (Hash vs. Nested Loop vs. Merge Join).
* [ ] **Task 3.2: SQL Viva & Interview Bank (Preview Free + ₹10 Full)**:
  * *Title:* "Top 45 SQL Viva Practical & Junior Interview Traps"
  * *Covers:* Index internals, clustered vs non-clustered, execution order of `GROUP BY` vs `WHERE`, practical query traps.
* [ ] **Task 3.3: Production Dataset 1 (Free with Login)**:
  * *Title:* "Indian E-Commerce 50,000 Orders Analytics Dataset"
  * Cleaned CSV, schema definition, and 10 real-world business analysis practice questions.
* [ ] **Task 3.4: Python Real-World Foundations (Free)**:
  * *Title:* "Python Memory, References & The Mutable Default Argument Trap".

### Phase 4: UPI Micro-Purchases & Checkout Pipeline
* [ ] **Task 4.1**: Set up `digital_products` and `user_purchases` tables.
* [ ] **Task 4.2**: Integrate a frictionless Indian payment gateway (Razorpay / Cashfree) supporting 1-click UPI QR and UPI app intents for ₹10 / ₹20 / ₹99 transactions.
* [ ] **Task 4.3**: Add purchase confirmation and instant digital delivery/unlock view.

### Phase 5: Cohort Funnel Attribution & SEO Automation
* [ ] **Task 5.1**: Build contextual cohort callout partials (`app/templates/library/partials/cohort_card.html`) with dynamic attribution parameters (e.g., `/register?source=library_sql_joins`).
* [ ] **Task 5.2**: Generate dynamic `sitemap.xml` automatically indexing all library notes, practice sets, and datasets.
* [ ] **Task 5.3**: Inject JSON-LD structured schemas (`TechArticle`, `FAQPage`, and `Dataset`) for rich Google search snippets.

---

## 7. Standard 5-Part Content Blueprint (For Every Note)

Whenever a note or guide is authored for the Mythos Library, it must follow this exact structure:

1. **Academic Definition & Core Concept:** Rigorous, textbook-clean explanation suitable for scoring full marks in a university written exam.
2. **Interactive Code & Query Examples:** Self-contained, copyable, syntax-highlighted examples with expected outputs.
3. **The Production Reality ("What Textbooks Skip"):** Real-world edge cases, performance implications, memory/disk trade-offs, and how senior engineers handle it.
4. **Exam & Interview Gotchas:** 3–5 high-frequency tricky questions examiners and interviewers ask to catch students off guard.
5. **Mythos Mentorship Bridge:** A one-sentence contextual bridge inviting readers to apply for the live hands-on Weekend Cohort.
