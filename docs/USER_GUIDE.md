# Student Admission & Course Platform — User Guide

Hi Shubham! 👋

This guide explains how your new student admission system works, how to run it locally on your computer, how database persistence works on Render.io, and how to view and download student registrations.

---

## 1. What Has Been Built?

We are transforming your website from a simple resume into an **active training and student enrollment hub**:
* **Who You Are**: Visitors see you as the **Lead Instructor & Consultant** (3+ years experience, 120+ developers trained).
* **Course Subject**: **Data Analysis** covering **Python, SQL, Power BI, Excel, and Tableau**.
* **Fixed Schedule**: **Saturday and Sunday only, 6:00 PM to 8:00 PM IST**.
* **No Public Fees**: As requested, **no fees or prices are shown anywhere on the website**. You discuss fees privately with students when counseling them.
* **Two Ways for Students to Register**:
  1. **General Enquiry**: If they have questions about the syllabus, want a callback, or need counseling.
  2. **Batch Registration**: If they want to reserve a seat in your upcoming weekend batch.

---

## 2. The Render.io & Database Question Explained Simply

> **Why you were right to be concerned about SQLite:**
> * On Render's free tier, the computer running your website is temporary (called an "ephemeral container").
> * If you save data into a local SQLite file (like `portfolio.db`), Render deletes that file whenever the server restarts or updates. That means student registrations would be lost!

> **The Easy & Free Solution:**
> * You can connect a **free cloud PostgreSQL database** that keeps all your student data permanently safe.
> * Services like **[Neon.tech](https://neon.tech)** or **[Supabase.com](https://supabase.com)** give you a 100% free permanent database in under 2 minutes.
> * When deploying to Render, you simply add one setting:
>   * Name: `DATABASE_URL`
>   * Value: Paste the link from Neon or Supabase (e.g., `postgresql://user:pass@ep-cool-db.neon.tech/neondb`)
> * **On your local laptop**: You don't have to install anything! The code automatically detects you are on your PC and uses local SQLite (`course_platform.db`) for testing.

---

## 3. How to Run the Website on Your Computer

1. Open your terminal or PowerShell in your project folder (`f:\Projects\coding`).
2. Run this command:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
3. Open your browser:
   * **Website**: [http://localhost:8000](http://localhost:8000)
   * **Interactive API Playground**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 4. How to Test Student Registrations Right Now

You can test submitting students right from your browser using the Swagger Docs at [http://localhost:8000/docs](http://localhost:8000/docs):

1. Go to `http://localhost:8000/docs`.
2. Look for the **Courses & Admissions** section.
3. Click on **`POST /api/courses/register`** (or `POST /api/courses/enquiry`), click **Try it out**, fill in a test name and phone number, and click **Execute**.
4. You will get a instant confirmation response showing the student is registered!

---

## 5. How to Download All Student Leads (Excel / CSV)

You can download a clean spreadsheet of all students who registered or enquired anytime:
* Simply visit: **[http://localhost:8000/api/courses/leads/export.csv](http://localhost:8000/api/courses/leads/export.csv)**
* Your browser will instantly download a `.csv` file with columns for:
  * Student Name
  * Email
  * WhatsApp / Phone number
  * Current status (Student, Working Professional, Fresher)
  * Experience level
  * Questions or notes
  * Date & time submitted

You can open this CSV directly in Microsoft Excel, Google Sheets, or send it to your phone.

---

## 6. What's Next?

* The **backend foundation is 100% complete and tested**.
* Next, we will design the **frontend user interface**:
  * Modern hero banner introducing you as the Data Analysis instructor.
  * Clear syllabus breakdown (Python, SQL, Power BI, Excel, Tableau).
  * Prominent schedule banner ("Saturday & Sunday | 6:00 PM – 8:00 PM").
  * Clean, interactive pop-up forms for "Enroll Now" and "Ask a Question".
