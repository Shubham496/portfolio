# AI Agent Directives & Operational Rules (AGENTS.md / agent.md)

> **PRIMARY DIRECTIVE FOR ALL AI AGENTS & CODING ASSISTANTS**:
> You are working on the **MYTHOS Online Institute** repository.
> You must strictly observe the non-negotiable operational rules below on every task.

---

## 1. The 16 Golden Rules for AI Agents

1. **Read `GUIDE.md` before starting development**: Understand the current application state, purpose, tech stack, and constraints before proposing or writing code.
2. **Read the latest 15 entries in `Changeslog.md`**: Familiarize yourself with recent feature additions, schema migrations, and architectural decisions.
3. **Do not read the complete archive unless historical context is relevant**: Avoid context window pollution by reading `docs/CHANGELOG_ARCHIVE.md` only when specifically debugging legacy behavior or historical decisions.
4. **Inspect actual source code before making assumptions**: Never guess signatures, route paths, database columns, or template structures; always verify the current code directly.
5. **Check Git status before modifying anything**: Inspect `git status` at the start of every session to ensure the working tree is clean and understand any unstaged work.
6. **Execute work in bounded, incremental slices (Max 1–2 subtasks per turn)**: When asked to work on a phase or multi-task roadmap, **never attempt the entire phase at once**. Implement strictly **1 or 2 cohesive subtasks**, verify them, commit locally, document progress, and leave subsequent tasks for the user's next prompt.
7. **Follow the existing architecture and conventions**: Respect modular sub-app boundaries (`app/apps/`), dual-engine database design, and template section partial patterns.
8. **Avoid unnecessary refactoring**: Do not re-architect functioning modules, rename working files, or introduce new paradigms unless explicitly requested by the platform owner.
9. **Never delete working functionality without approval**: Preserve existing features, test cases, and working code paths.
10. **Keep edits surgical and compact (<50 lines)**: Avoid massive monolithic file replacements in complex HTML or Python templates. Read exact line ranges first, match exact whitespace, and apply compact contiguous replacements to eliminate edit tool mismatch errors.
11. **Leverage fast targeted testing during iteration**: Use targeted pytest runs (`pytest tests/test_courses.py -k <test_name>`) for rapid 1-second feedback loops during development; execute the full test suite (`python -m pytest -v`) only once as the final verification gate before completing the turn.
12. **Never expose credentials or API keys**: Keep secrets strictly in `.env`. Never commit, log, or document passwords, tokens, or private hashes. Ensure `.env` and `*.db` remain in `.gitignore`.
13. **Test important changes before declaring completion**: Verify that all automated tests pass cleanly (`75+ passed, 0 failures`) before completing a task slice.
14. **Update `Changeslog.md` after meaningful changes**: Document every meaningful feature, schema change, bug fix, or breaking change following the standardized changelog entry format.
15. **Archive older entries when the 15-entry limit is exceeded**: Automatically transfer entries older than the latest 15 to `docs/CHANGELOG_ARCHIVE.md` preserving all technical details.
16. **Never modify production data or execute destructive operations without approval**: Do not drop tables, wipe rows, alter production databases, or execute destructive DDL commands.

---

## 2. Non-Negotiable Push & Deployment Boundary

> [!CAUTION]
> **STRICT PUSH RESTRICTION (PLATFORM OWNER ONLY)**:
> **Only the human platform owner ("I") is authorized to push commits to the remote repository (`git push origin main`) or trigger production deployments.**
> AI agents and automated scripts are **STRICTLY PROHIBITED** from executing `git push`.
> Agents must verify tests, review `git status`, stage files, and commit locally with conventional commit messages (`feat:`, `fix:`, `refactor:`, `docs:`), leaving the local working tree clean for the platform owner to review and push.

---

## 3. Standard Development & Task Completion Lifecycle (Single-Slice Work Unit)

When assigned a task or asked to perform a roadmap phase, follow this exact single-slice lifecycle:

```
Step 1: Slice Scoping & Boundary Definition
  ├─ Inspect docs/task_new.md to find the active phase
  ├─ Select ONLY the next 1 or 2 pending subtasks (e.g. Task 5.1 only)
  ├─ Explicitly state which subtask(s) you are implementing in this turn
  └─ DO NOT attempt the remaining tasks of the phase in this execution

Step 2: Ingest Context & Baseline Check
  ├─ Ingest only files relevant to the scoped subtask(s)
  ├─ Run: git status (confirm clean state)
  └─ Run targeted test baseline: pytest tests/test_<module>.py -k <relevant_test>

Step 3: Surgical Implementation
  ├─ Follow domain boundaries (app/apps/courses, app/apps/library, app/apps/todos)
  ├─ Apply small, focused edits (<50 lines per edit block) to prevent tool failures
  ├─ Adhere to zero-code execution on platform rule (static syntax only)
  └─ Maintain zero upfront pricing on student browse surfaces

Step 4: Two-Tier Verification
  ├─ Fast tier: pytest tests/test_<module>.py -k <new_or_modified_test> (instant feedback)
  └─ Regression tier: python -m pytest -v (full suite must pass cleanly with 0 errors)

Step 5: Documentation & Task Tracking
  ├─ Check off completed subtask(s) in docs/task_new.md (e.g. change [ ] to [x])
  ├─ Update Changeslog.md with new entry (date, features, files, APIs, schemas, fixes)
  ├─ If Changeslog.md exceeds 15 entries, transfer oldest to docs/CHANGELOG_ARCHIVE.md
  └─ Update GUIDE.md if current architecture, endpoints, or schemas changed

Step 6: Local Git Hygiene & Clear Handoff
  ├─ Stage modified files: git add <files>
  ├─ Create clean commit: git commit -m "type(scope): clear description of this slice"
  ├─ DO NOT RUN GIT PUSH
  └─ Report back to user:
       1. What was completed in this slice
       2. Tests verified and passing count
       3. Remaining subtasks in the current phase
       4. Clear prompt suggestion for the user to trigger the next slice
```

---

## 4. Incremental Phase Execution & Slicing Protocol

To avoid long wait times, context saturation, and edit errors, agents must adhere to the following slicing protocol:

1. **Phase Chunking Size**:
   - **Small tasks** (e.g., config changes, single API endpoint, simple UI card): 1 to 2 tasks per instruction.
   - **Medium/Large tasks** (e.g., new database table + schema migration + complex admin UI table): **Strictly 1 task per instruction**.
2. **Explicit Slice Declaration**:
   - At the beginning of the turn, declare:  
     > *"Working on [Phase X: Task X.Y] — Scoping this turn to Task X.Y only."*
3. **No Unprompted Phase Run-on**:
   - Even if the user says "perform next phase", **execute only the first slice (Task X.1 or X.1–X.2)**.
   - Conclude by stating what is ready and ask the user to confirm before moving to Task X.3.
4. **Preserved Working State**:
   - Each completed slice must leave the repository in a fully tested, working, and committed state. No half-finished or broken code between turns.

---

## 5. Key Implementation Constraints & Invariants

1. **Academic Focus**: Live online weekend cohorts in Data Analysis & Digital Marketing (`Saturday & Sunday, 6:00 PM – 8:00 PM IST`).
2. **Admissions & Pricing Rule**: **Zero public pricing** displayed for live cohorts on the public website; admissions and batch readiness are handled through counseling and `/register`. Digital student micro-assets (viva sets, notes) may display micro-prices (₹10–₹49) only at purchase gates.
3. **Student Contact Fields**: Email is **strictly optional** across student registration and enquiry forms. Only **Full Name** and **WhatsApp/Phone** are mandatory.
4. **Zero Code Execution**: The platform is strictly an educational reading and copy-only reference; never provide interactive runners, consoles, or REPLs.
5. **Decoupled Asset Vault**: High-res images, datasets, and downloadable zip archives must be housed in `external_assets/` and referenced via CDN/Raw URLs, never committed directly to the core application repository.
