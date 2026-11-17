# AI Agent Directives & Operational Rules (AGENTS.md)

> **PRIMARY DIRECTIVE FOR ALL AI AGENTS & CODING ASSISTANTS**:
> You are working on the **MYTHOS Online Institute** repository.
> You must strictly observe the non-negotiable operational rules below on every task.

---

## 1. The 15 Golden Rules for AI Agents

1. **Read `GUIDE.md` before starting development**: Understand the current application state, purpose, tech stack, and constraints before proposing or writing code.
2. **Read the latest 15 entries in `Changeslog.md`**: Familiarize yourself with recent feature additions, schema migrations, and architectural decisions.
3. **Do not read the complete archive unless historical context is relevant**: Avoid context window pollution by reading `CHANGELOG_ARCHIVE.md` only when specifically debugging legacy behavior or historical decisions.
4. **Inspect actual source code before making assumptions**: Never guess signatures, route paths, database columns, or template structures; always verify the current code directly.
5. **Check Git status before modifying anything**: Inspect `git status` at the start of every session to ensure the working tree is clean and understand any unstaged work.
6. **Follow the existing architecture and conventions**: Respect modular sub-app boundaries (`app/apps/`), dual-engine database design, and template section partial patterns.
7. **Avoid unnecessary refactoring**: Do not re-architect functioning modules, rename working files, or introduce new paradigms unless explicitly requested by the platform owner.
8. **Never delete working functionality without approval**: Preserve existing features, test cases, and working code paths.
9. **Never expose credentials or API keys**: Keep secrets strictly in `.env`. Never commit, log, or document passwords, tokens, or private hashes. Ensure `.env` and `*.db` remain in `.gitignore`.
10. **Test important changes before declaring completion**: Always execute the automated test suite (`python -m pytest -v`) and verify that all tests pass cleanly before completing a task.
11. **Update `Changeslog.md` after meaningful changes**: Document every meaningful feature, schema change, bug fix, or breaking change following the standardized changelog entry format.
12. **Update `GUIDE.md` whenever current architecture or functionality changes**: Keep the single-source-of-truth manual aligned with the code.
13. **Archive older entries when the 15-entry limit is exceeded**: Automatically transfer entries older than the latest 15 to `CHANGELOG_ARCHIVE.md` preserving all technical details.
14. **Never invent project information or document unverified functionality**: Ground every technical statement in verified code. Mark untested features clearly as unverified.
15. **Never modify production data or perform destructive database operations without approval**: Do not drop tables, wipe rows, alter production databases, or execute destructive DDL commands.

---

## 2. Non-Negotiable Push & Deployment Boundary

> [!CAUTION]
> **STRICT PUSH RESTRICTION (PLATFORM OWNER ONLY)**:
> **Only the human platform owner ("I") is authorized to push commits to the remote repository (`git push origin main`) or trigger production deployments.**
> AI agents and automated scripts are **STRICTLY PROHIBITED** from executing `git push`.
> Agents must verify tests, review `git status`, stage files, and commit locally with conventional commit messages (`feat:`, `fix:`, `refactor:`, `docs:`), leaving the local working tree clean for the platform owner to review and push.

---

## 3. Standard Development & Task Completion Lifecycle

When assigned a task, follow this exact workflow:

```
Step 1: Ingest Context
  ├─ Read GUIDE.md
  ├─ Read the latest entries in Changeslog.md
  └─ Inspect relevant files in app/ and tests/

Step 2: Pre-Execution Verification
  ├─ Run: git status (confirm clean state)
  └─ Run: python -m pytest -v (confirm baseline passes)

Step 3: Implementation
  ├─ Follow domain boundaries (app/apps/courses, app/apps/library, app/apps/todos)
  ├─ Adhere to zero-code execution on platform rule (static syntax only)
  └─ Maintain zero upfront pricing on student browse surfaces

Step 4: Post-Implementation Verification
  ├─ Run: python -m pytest -v (must pass with 0 errors)
  └─ Run: git status (ensure no untracked scratch files remain)

Step 5: Documentation Maintenance
  ├─ Update Changeslog.md with new entry (date, features, files, APIs, schemas, fixes)
  ├─ If Changeslog.md exceeds 15 entries, transfer oldest to CHANGELOG_ARCHIVE.md
  └─ Update GUIDE.md if current architecture, endpoints, or schemas changed

Step 6: Local Git Hygiene
  ├─ Stage modified files: git add <files>
  ├─ Create clean commit: git commit -m "type(scope): clear description"
  └─ DO NOT RUN GIT PUSH
```

---

## 4. Key Implementation Constraints & Invariants

1. **Academic Focus**: Live online weekend cohorts in Data Analysis & Digital Marketing (`Saturday & Sunday, 6:00 PM – 8:00 PM IST`).
2. **Admissions & Pricing Rule**: **Zero public pricing** displayed for live cohorts on the public website; admissions and batch readiness are handled through counseling and `/register`. Digital student micro-assets (viva sets, notes) may display micro-prices (₹10–₹49) only at purchase gates.
3. **Student Contact Fields**: Email is **strictly optional** across student registration and enquiry forms. Only **Full Name** and **WhatsApp/Phone** are mandatory.
4. **Zero Code Execution**: The platform is strictly an educational reading and copy-only reference; never provide interactive runners, consoles, or REPLs.
5. **Decoupled Asset Vault**: High-res images, datasets, and downloadable zip archives must be housed in `external_assets/` and referenced via CDN/Raw URLs, never committed directly to the core application repository.
