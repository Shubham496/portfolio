# Cloud Deployment & Infrastructure Specification (Render.io)

## 1. Deployment Overview & Architecture

**MYTHOS Online Institute** is configured for automated cloud deployment on **Render.io** as a Web Service. The deployment infrastructure is defined as code in [`render.yaml`](file:///f:/Projects/coding/render.yaml) and [`Procfile`](file:///f:/Projects/coding/Procfile).

```
 ┌──────────────────────┐
 │ Local Repository     │
 │ (Platform Owner)     │
 └──────────┬───────────┘
            │ git push origin main (Owner ONLY)
            ▼
 ┌──────────────────────┐
 │ GitHub Repository    │ (Branch: main)
 └──────────┬───────────┘
            │ Webhook Trigger
            ▼
 ┌────────────────────────────────────────────────────────┐
 │ Render.io Build Environment                            │
 │ • Runtime: Python 3.10.11                              │
 │ • Build: pip install -r requirements.txt               │
 └──────────────────────────┬─────────────────────────────┘
                            │ Build Success
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ Render.io Web Container                                │
 │ • Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT │
 │ • Port Binding: Binds dynamically to $PORT             │
 │ • Memory Envelope: 40-60 MB baseline                   │
 └──────────────────────────┬─────────────────────────────┘
                            │ Health Probe
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ Health Verification                                    │
 │ • Endpoint: GET /health (HTTP 200 OK)                  │
 │ • Traffic cutover to active container                  │
 └────────────────────────────────────────────────────────┘
```

---

## 2. Infrastructure Parameters

| Parameter | Configuration Value | Source File / Location |
| :--- | :--- | :--- |
| **Service Name** | `shubham-portfolio` | `render.yaml:3` |
| **Service Type** | Web Service (`web`) | `render.yaml:2` |
| **Environment Runtime**| `python` (Python 3.10.11) | `render.yaml:4, 11` |
| **Deployment Branch**| `main` | GitHub integration tracking branch |
| **Build Command** | `pip install -r requirements.txt` | `render.yaml:5` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | `render.yaml:6`, `Procfile:1` |
| **Health Check Path**| `/health` | `app/main.py:259` |
| **Auto-Deploy** | Yes (Enabled on commits to `main`) | Render dashboard service setting |

---

## 3. Environment Variable Specification

> [!WARNING]
> **Zero-Secret Leak Guard**: Never commit real credentials, passwords, or production keys into Git. All production secrets must be entered directly into the **Render Dashboard Environment Settings**.

| Variable Name | Required | Default Fallback | Purpose & Guidance |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | Yes | `production` | Switches config dispatcher to `DeploymentSettings`. Set in `render.yaml`. |
| `PYTHON_VERSION`| Yes | `3.10.11` | Ensures Render provisions the verified Python runtime. Set in `render.yaml`. |
| `DATABASE_URL` | **Critical**| `""` (falls back to local SQLite) | Connection string for persistent Cloud PostgreSQL (e.g. Neon.tech, Supabase, Render Postgres). Must be set manually in Render dashboard. |
| `PORT` | Auto | `10000` | Injected dynamically by Render container environment; bound by Uvicorn. |
| `ADMIN_PASSWORD`| Recommended| Loaded from `.env` in dev | Master instructor password for the `admin` profile (`admin@mythostech.in`). |
| `AGENT_PASSWORD`| Recommended| Loaded from `.env` in dev | Dedicated password for automated test/agent profile (`agent@mythostech.in`). |
| `SECRET_KEY` | Recommended| Safe built-in fallback | Cryptographic secret for signing session cookies (`URLSafeTimedSerializer`). |

---

## 4. End-to-End Deployment Lifecycle

### Step 1: Pre-Deployment Local Verification
Before publishing updates, the platform owner confirms the local environment is sound:
```powershell
# 1. Verify full automated test suite passes (all 32 tests)
python -m pytest -v

# 2. Verify git status is clean with no untracked secrets
git status
```

### Step 2: Push to GitHub (Owner Authority)
> [!IMPORTANT]
> **Strict Push Restriction**: AI agents and automated scripts are **strictly prohibited** from running `git push`. Only the human platform owner can publish commits to remote.

```powershell
git push origin main
```

### Step 3: Render Ingestion & Build Phase
1. Render receives the GitHub push notification via webhook.
2. An isolated build container clones `main`.
3. Render sets `PYTHON_VERSION=3.10.11` and installs virtualenv.
4. Executes:
   ```bash
   pip install -r requirements.txt
   ```
5. Dependencies are cached across builds to accelerate future deployments.

### Step 4: Container Execution & Health Check
1. The container launches the ASGI application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
2. Render issues a periodic health probe to `GET /health`.
3. Route handler verifies application health:
   ```json
   {
     "status": "healthy",
     "owner": "Shubham Singh",
     "app": "MYTHOS Online Institute",
     "version": "2.2.0",
     "memory_friendly": true
   }
   ```
4. Upon receiving HTTP 200, Render directs public internet traffic to the new container and safely spins down the old instance with zero downtime.

---

## 5. Ephemeral Filesystem & Database Persistence Strategy

> [!CAUTION]
> **Ephemeral Container Warning**: Render's free and standard web containers possess **ephemeral filesystems**. When a container restarts, redeploys, or wakes up from idle sleep, any files created locally on disk (including SQLite `.db` files) are erased.

### The Solution: External PostgreSQL Persistence
To preserve student leads, batch enrollments, and admin accounts permanently:
1. Provision a free PostgreSQL database on **[Neon.tech](https://neon.tech)**, **[Supabase.com](https://supabase.com)**, or **Render PostgreSQL**.
2. Copy the database connection URL (e.g. `postgresql://user:password@ep-host.region.neon.tech/neondb?sslmode=require`).
3. In Render Dashboard &rarr; Service &rarr; **Environment** &rarr; Add Environment Variable:
   - Key: `DATABASE_URL`
   - Value: `<your-postgres-connection-string>`
4. The application automatically normalizes legacy `postgres://` URLs to `postgresql://` and activates connection pooling (`pool_pre_ping=True`, `pool_recycle=300`).

---

## 6. Common Deployment Failures & Troubleshooting

### 1. Build Failure: Missing Python Dependencies or Incompatible Wheels
- **Symptom**: Build log shows `Command 'pip install -r requirements.txt' failed with exit code 1`.
- **Root Cause**: Installing C-extension packages without pre-compiled binary wheels (e.g. `psycopg2` vs `psycopg2-binary`).
- **Resolution**: Ensure `requirements.txt` specifies `psycopg2-binary>=2.9.9` and version bounds compatible with Python 3.10.

### 2. Application Crash: `Port binding failed` / `Address already in use`
- **Symptom**: Service immediately transitions to "Crashed" or times out during startup.
- **Root Cause**: Hardcoding port `8000` instead of reading the dynamic `$PORT` environment variable.
- **Resolution**: Always use `--port $PORT` in both `render.yaml` and `Procfile`.

### 3. Database Connection Dropped / Timeout on Idle Wakeup
- **Symptom**: First visitor after 15 minutes of inactivity receives HTTP 500 Internal Server Error.
- **Root Cause**: Serverless Postgres (like Neon) suspended compute; stale socket remained in pool.
- **Resolution**: Verified active in code: `pool_pre_ping=True` tests connection health and transparently reconnects.

### 4. Slug Size Exceeded (> 500 MB)
- **Symptom**: Render build fails with disk quota exceeded error.
- **Root Cause**: Accidental inclusion of large datasets, video files, or high-res images in Git.
- **Resolution**: Ensure large files live in `external_assets/` (which is git-ignored) and serve via jsDelivr CDN or GitHub Raw links.

---

## 7. Rollback Procedures

### Method 1: Instant 1-Click Rollback via Render Dashboard (Fastest)
1. Open the **Render Dashboard** &rarr; Select Web Service (`shubham-portfolio`).
2. Navigate to the **Deploys** tab.
3. Locate the last known healthy deployment (marked with a green checkmark).
4. Click the three dots (`...`) on the right side of that deploy &rarr; Select **Rollback to this deploy**.
5. Render immediately redeploys the prior build artifact without re-running `pip install`.

### Method 2: Git Rollback (Audit Trail Method)
If a faulty commit was pushed to `main`:
1. Revert the problematic commit locally:
   ```powershell
   git revert <faulty-commit-sha>
   ```
2. Run the automated tests to ensure green status:
   ```powershell
   python -m pytest -v
   ```
3. Platform owner pushes the revert commit:
   ```powershell
   git push origin main
   ```
4. Render automatically builds and deploys the clean revert commit.
