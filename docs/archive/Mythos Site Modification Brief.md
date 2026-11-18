# Mythos Site Modification Brief

For the AI coding agent working on the MYTHOS Online Institute repo (FastAPI + Jinja2, mythostech.in) · Prepared Nov 19, 2026

## How to use this document

Give this document to your AI agent together with the repo, and ask for **one phase at a time**. Review and test each phase yourself before moving on. Starter prompt to paste:

```
You are working on the MYTHOS Online Institute repo. First read AGENTS.md, GUIDE.md and this brief completely. Implement Phase 0 only, then stop and report: what changed, which tests were run, and which [PLACEHOLDER] items still need my input. Never run git push. Never invent names, numbers, testimonials or credentials: use a [BRACKETED] placeholder instead. Commit locally with conventional commit messages after the tests pass.
```

## Goal of the site

The site is a **lead machine for live cohorts**, not a shop for Rs 10 items. Its job, in order: get found on Google, build trust, capture name + WhatsApp number, move people to a free demo class, and enrol them in a cohort. Small bundle sales are a bonus, built last.

## Rules that must NOT change

- Only the owner runs git push or deploys. The agent tests, stages and commits locally and leaves git status clean.
- Never commit .env, passwords, tokens or \*.db files.
- Zero code execution on the platform: code blocks stay static and copy-only.
- No cohort tuition or prices on public pages. A price appears only at a paywall or when someone clicks to buy.
- Email stays optional on all forms; Full Name and Phone/WhatsApp stay mandatory.
- Admin portal stays hidden (no public links; signup disabled).
- Top bar links between pages; left rail navigates within a page.
- Every change updates CHANGELOG and the guides, and the full test suite must pass.

## Owner-approved changes to existing rules

These override the old guide where they conflict. Update the guide files to match.

1. **Two mentors.** The Digital Marketing mentor (the owner's partner) appears with real name and photo. The Data Analytics mentor stays anonymous: no name, no photo, shown as the Mythos Data Analytics Mentor.
2. **One subject at a time.** The Data Analytics track runs one subject per batch (about 8 weeks): SQL, Excel, Power BI, Python, Tableau, Git and GitHub. The site shows what is enrolling now and what comes next.
3. **Track schedules.** Data Analytics batches run Saturday and Sunday, 6 to 8 PM IST. Digital Marketing batches use their own schedule \[DM\_SCHEDULE\]. Schedule fields are per batch, not global.
4. **Trust claim.** Remove every use of 550+ Students Trained. Replace with the text in \[TRUST\_CLAIM\], default: 400+ learners taught by our mentors over 3+ years. The owner confirms the wording.
5. **Contact details.** Business email and WhatsApp come from environment variables, not hardcoded.

## Placeholders only the owner can supply

- &#91;DM\_MENTOR\_NAME\], \[DM\_MENTOR\_PHOTO\], \[DM\_MENTOR\_BIO\], \[DM\_MENTOR\_LINKEDIN\]
- &#91;DM\_SCHEDULE\] and the DM batch codes and start dates
- &#91;BUSINESS\_EMAIL\], \[BUSINESS\_WHATSAPP\]
- &#91;WHATSAPP\_CHANNEL\_URL\], \[TELEGRAM\_URL\], \[INSTAGRAM\_URL\], \[LINKEDIN\_PAGE\_URL\], \[YOUTUBE\_URL\]
- &#91;GOOGLE\_SITE\_VERIFICATION\] token
- &#91;SUBJECT\_ORDER\] for Data Analytics (default: SQL, Excel, Power BI, Python, Tableau, Git and GitHub)
- &#91;DEMO\_CLASS\_DATETIME\] and meeting link
- &#91;LEAD\_MAGNET\_FILES\] (cheat sheet, dataset) hosted in external\_assets
- Testimonials: real ones only

## Phase 0: Security and privacy (do first)

The site is about to collect many more phone numbers, so this comes before anything else.

- **0.1 Lock the lead API.** The guide lists /api/courses/leads, /leads/summary, /leads/export.csv, /leads/{id} and PATCH /leads/{id}/status under the public API. Verify whether they require an admin session. If any are reachable anonymously, protect them with require\_admin or remove them. Only enquiry, register, batches and instructor info stay public. Add tests proving anonymous requests are rejected.
- **0.2 SECRET\_KEY.** Remove the hardcoded fallback value from code and docs. In production, refuse to start if SECRET\_KEY is missing. The owner then rotates the key.
- **0.3 Consent and policies.** Add /privacy, /terms and /refund-policy pages with plain-language placeholder text for the owner to review. Add a required consent checkbox to every form ('I agree to be contacted by phone or WhatsApp about this course'). Store consent flag and timestamp. Add a do\_not\_contact lead status.
- **0.4** Never write phone numbers or emails to application logs.

## Phase 1: Be findable (SEO)

- **1.1** Dynamic /sitemap.xml and /robots.txt (disallow /admin and /api, point to the sitemap).
- **1.2** Unique title, meta description, canonical URL and Open Graph tags on every page. Base URL comes from an environment variable.
- **1.3** Render a Google Search Console verification meta tag from GOOGLE\_SITE\_VERIFICATION when set.
- **1.4** JSON-LD: Organization on the home page, Course for batches, TechArticle for hand-written notes only.
- **1.5 Content quality gate.** Add a frontmatter field status: published or draft. Pages synthesized from templates (the 34-technology catalog) are treated as draft: noindex meta tag, excluded from the sitemap, and shown in the sidebar as Coming soon with no fake body. Counts shown in the library include only published notes. The agent must not generate filler content to fill gaps.
- **1.6 Performance.** Cache headers for static files, gzip, lazy-loaded images, no render-blocking scripts. Keep /health suitable for an external uptime pinger.
- **1.7** Breadcrumbs, previous/next links, and a contextual demo-class CTA on every note.

## Phase 2: Trust and people

- **2.1 Mentors section** on the home page and a new /about page. DM mentor: name, photo, bio, LinkedIn from the placeholders. Data Analytics mentor: anonymous, with a neutral bio (3+ years teaching, 400+ learners taught, tools covered). Each profile claims only what that person actually did. The DM mentor is never presented as teaching data analytics, and vice versa.
- **2.2** Replace the 550+ claim everywhere: templates, API output, generated syllabus PDF, tests.
- **2.3 Contact cleanup.** Move email and WhatsApp to BUSINESS\_EMAIL and BUSINESS\_WHATSAPP. Remove the old values from templates, base\_config, services, the PDF generator, docs and tests. Regenerate the syllabus PDF.
- **2.4 Testimonials component** that stays hidden until real entries exist. Never fabricate quotes, names or results.
- **2.5** Remove any wording that implies guaranteed jobs or salaries.

## Phase 3: Cohort display

- **3.1** The cohort section reads from the Batch table and groups by track. Each track shows Now enrolling, Running, and Next. Completed batches move to Past batches.
- **3.2 Data Analytics roadmap strip** showing \[SUBJECT\_ORDER\] with the current subject highlighted and text such as 'One subject per batch so you go deep.' Add a Notify me for the next batch button that creates a waitlist lead with the chosen subject.
- **3.3 Digital Marketing track** shows its own schedule and mentor from the batch record.
- **3.4 Admin batch manager.** In the admin portal, add a simple list and form to create, edit and close batches (code, title, track, subject, mentor, days, time, start date, seats, status) so no code change is needed to add a batch.
- **3.5** Show seats left as a number. No prices.

## Phase 4: Lead capture and funnel

- **4.1 Data model.** Add lead types demo\_class, waitlist and lead\_magnet. Add columns: source (utm\_source, utm\_medium, utm\_campaign, referrer), subject\_interest, consent\_at, follow\_up\_date. Add an idempotent startup migration that works on both SQLite and PostgreSQL (create\_all will not add columns to existing tables).
- **4.2 Demo class page** at /demo: next session date and time (editable in admin), form (name, WhatsApp, optional email, subject interest, consent), confirmation page with Add to calendar and the WhatsApp channel link.
- **4.3 Lead magnets.** On each subject hub and note sidebar: 'Download the free \[SQL interview cheat sheet / practice dataset\]'. A short form (name, WhatsApp, consent) reveals the link after submission. Notes themselves stay fully open with no login wall.
- **4.4 Join buttons** for the WhatsApp channel and Telegram in the footer, note sidebar and confirmation pages.
- **4.5 UTM capture.** Store UTM parameters on first visit in a cookie and attach them to any lead created later.
- **4.6 Admin pipeline.** Statuses: new, contacted, demo\_attended, enrolled, closed, do\_not\_contact. Filters by lead type, source and subject. Follow-up date and notes. Admin-only CSV export including source and consent.
- **4.7 Spam protection.** Honeypot field and rate limiting on all public form endpoints.

## Phase 5: Analytics

- **5.1** Privacy-friendly analytics (Plausible or Umami script from environment variables) or a GA4 ID. Events: cta\_click, form\_submit, lead\_magnet\_download, whatsapp\_join.
- **5.2** An admin funnel card: leads this week by source, demo attendees, enrolments.

## Phase 6: Later only, when the owner says so

An optional paid bundle using an external payment link from an environment variable, with the price shown only at the gate. No student login system or payment gateway build until there is steady traffic or paying customers.

## Testing and delivery rules

- All existing tests pass, plus new tests for: sitemap and robots, noindex on draft pages, anonymous access rejected on lead endpoints, no old personal email or phone in rendered pages, no 550+ string, no currency symbols on browse pages, consent required on forms, and a demo form creating a lead with source data.
- One small commit per task. Update CHANGELOG and guides. Keep git status clean. Do not push.
- After each phase, report finished items and the placeholders still open.

## Definition of done

- The sitemap is submitted in Search Console and only hand-written pages are indexable.
- A visitor can register for a demo class or download a lead magnet in under a minute, and the lead appears in the admin pipeline with its source.
- The home page shows one enrolling Data Analytics subject, the roadmap, and the DM mentor's track.
- No personal contact details or unverifiable claims remain anywhere in the project.
