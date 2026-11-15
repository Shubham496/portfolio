# Student Admission & Course Platform — User Guide

Hi Shubham! 👋

This guide explains how your student admission platform works, how to run it locally on your computer, how to use the hidden admin portal with pagination and separated status/date tracking, how cloud database persistence works on Render.io, and how to export student leads.

---

## 1. What Has Been Built?

Your website is an **active online educational institute platform (MYTHOS Online Institute)**:
* **Brand & Institute**: **MYTHOS Online Institute** (High-rigor 100% online cohorts).
* **Multi-Course Offerings**:
  1. **Performance Marketing & Paid Advertising** (Meta Ads, Google Ads, GA4, Funnel CRO, ROAS Scaling).
  2. **SEO, Content Strategy & Social Media Growth** (Technical SEO, Semrush, Content Marketing, LinkedIn Growth).
  3. **Data Analysis & Business Intelligence Masterclass** (Python, SQL, Power BI, Advanced Excel, Tableau).
* **Fixed Schedule**: **Saturday and Sunday only, 6:00 PM to 8:00 PM IST** (live online cohorts).
* **Admissions Model**: Pure educational admissions without online pricing or payment gateways. Enrollment readiness and batch selection are reviewed directly during orientation.
* **Direct Contact**: Email (`shubhamsinghh057@gmail.com`) and WhatsApp (`+91 8727864157`).
* **Production Deployment Note**: Only you ("I") can push code to production (`git push`). AI agents maintain clean local git commits for every task without pushing to production.
* **Easy Application for Students**:
  1. **Batch Registration**: Select their preferred course track and apply for upcoming weekend batches (via `/register` or homepage modal). Email is optional—only name and WhatsApp/mobile number are required!
  2. **General Enquiry**: Select course of interest, ask curriculum questions, or request counseling callbacks.
* **Syllabus PDF Brochure**:
  - Download PDF: [http://localhost:8000/course/syllabus/download](http://localhost:8000/course/syllabus/download)
  - View in browser: [http://localhost:8000/course/syllabus](http://localhost:8000/course/syllabus)

---

## 2. Hidden Instructor Monitoring Portal (`/admin`)

To keep your homepage clean and student-focused, **there is NO login or admin button on the public website**. Only you know the secret URL:

1. **Sign In**: Go to **[http://localhost:8000/admin/login](http://localhost:8000/admin/login)**
   - **Username**: `admin`
   - **Password**: Provided securely in your private `.env` file (`ADMIN_PASSWORD`).
   - **Public Signup Disabled**: For security, registration is disabled on the admin portal. Only you can log in.
2. **Monitoring Dashboard**: Once logged in at **[http://localhost:8000/admin/dashboard](http://localhost:8000/admin/dashboard)**, you can:
   - **View Separated Status & Dates**: The leads table features distinct columns for **Submitted Date** (with IST time) and **Status** (New, Contacted, Enrolled, Closed).
   - **Interactive Pagination**: Navigate through leads easily (page 1, 2, 3...) and choose between 10, 25, or 50 leads per page.
   - **Filter & Search**: Filter by lead type (*Batch Registrations* vs *Course Inquiries*) or pipeline status (*New*, *Contacted*, *Enrolled*, *Closed*), and search by student name, email, or phone.
   - **Direct WhatsApp Chat**: Click any student's phone number to open a WhatsApp conversation immediately.
   - **Update Status & Notes**: Change a student's stage and save counseling notes (e.g. "Called on Nov 12, confirmed batch seat") with one click.
   - **One-Click CSV Export**: Download the entire student database anytime by clicking **Export CSV**.

---

## 3. How to Run the Website on Your Computer

1. Open PowerShell or Terminal in your project directory (`f:\Projects\coding`).
2. Run this command:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
3. Open your browser:
   * **Website**: [http://localhost:8000](http://localhost:8000)
   * **Weekend Batch Registration**: [http://localhost:8000/register](http://localhost:8000/register)
   * **Admin Login**: [http://localhost:8000/admin/login](http://localhost:8000/admin/login)
   * **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 4. The Render.io & Database Question Explained Simply

> **Why you were right to be concerned about SQLite:**
> * On Render's free tier, the computer running your website is temporary (called an "ephemeral container").
> * If you save data into a local SQLite file (like `course_platform.db`), Render deletes that file whenever the server restarts or updates.
>
> **The Easy & Free Solution:**
> * Connect a **free cloud PostgreSQL database** that keeps all your student data permanently safe.
> * Services like **[Neon.tech](https://neon.tech)** or **[Supabase.com](https://supabase.com)** give you a permanent free cloud database in under 2 minutes.
> * When deploying to Render, you simply add one setting:
>   * Name: `DATABASE_URL`
>   * Value: Paste the link from Neon or Supabase (e.g. `postgresql://user:pass@ep-cool-db.neon.tech/neondb`)
> * **On your local computer**: You don't have to install anything! The code automatically detects you are on your PC and uses local SQLite (`course_platform.db`) for testing.

---

## 5. How to Download All Student Leads (Excel / CSV)

You can download a clean spreadsheet of all students who registered or enquired anytime:
* Simply click the **Export CSV** button on your admin dashboard, or visit: **[http://localhost:8000/api/courses/leads/export.csv](http://localhost:8000/api/courses/leads/export.csv)**
* The file opens in Microsoft Excel or Google Sheets with columns for:
  * Full Name
  * WhatsApp / Phone number
  * Email (if provided)
  * Career status (Student, Working Professional, Fresher)
  * Experience level & Message
  * Admission status & Instructor notes
  * Exact Date & Time submitted
