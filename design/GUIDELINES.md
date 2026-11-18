# MYTHOS BRAND DESIGN SYSTEM & CERTIFICATE GUIDELINES

> **Purpose**: This directory serves as the centralized design repository and single source of truth for all brand styling, typography rules, color tokens, SVG vector logos, and specifications for generating student completion certificates, brochures, and marketing collateral.

---

## 1. Brand Identity & Core Values

* **Brand Wordmark**: **MYTHOS**
* **Brand Tagline**: `BUILD SKILLS. BUILD SYSTEMS. BUILD THE FUTURE.`
* **Visual Philosophy**: Precision engineering meets modern executive aesthetics. High-contrast dark backgrounds, illuminated radial gradients, clean sans-serif typography, and subtle tech accents.
* **Core Domains**: Data Architecture, Python ETL Pipelines, Relational SQL Modeling, Business Intelligence (Power BI, Tableau), and Financial Spreadsheets (Excel).

---

## 2. Typography Specifications

### Primary Font Family: **Poppins**
* **Source**: Google Fonts ([https://fonts.google.com/specimen/Poppins](https://fonts.google.com/specimen/Poppins))
* **CSS Import**:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  ```
* **Fallback Stack**: `'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
* **Weights & Use Cases**:
  - `300 (Light)`: Secondary legal notes, subtle captions, fine print.
  - `400 (Regular)`: Body copy, syllabus descriptions, bulleted details.
  - `500 (Medium)`: Navigation items, form input labels, button labels.
  - `600 (SemiBold)`: Section subheadings, card titles, certificate award prefixes.
  - `700 (Bold)`: Main section headings (H2/H3), candidate name on certificates.
  - `800 (ExtraBold)`: Hero main headline, numerical milestone metrics (e.g. `400+`).
  - `900 (Black)`: Brand Wordmark (`MYTHOS`), Certificate Header.

### Monospace Font Family: **JetBrains Mono**
* **Fallback Stack**: `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`
* **Weights**: `400 (Regular)`, `500 (Medium)`, `700 (Bold)`
* **Use Cases**: Certificate verification IDs (e.g., `MYTHOS-DA-2026-B1042`), code snippets, terminal commands, phone numbers, and timestamps.

---

## 3. Official Color Palette & Design Tokens

### Core Neutral & Background Colors
| Token Name | HEX | RGB | Purpose |
| :--- | :--- | :--- | :--- |
| **Dark Navy Deep** | `#070B14` | `rgb(7, 11, 20)` | Primary website canvas, dark background. |
| **Card Navy** | `#0B1120` | `rgb(11, 17, 32)` | Card background, container surfaces. |
| **Surface Slate** | `#0F172A` | `rgb(15, 23, 42)` | Elevated modals, table headers, dark certificate borders. |
| **Border Slate** | `#1E293B` | `rgb(30, 41, 59)` | Structural lines, card borders. |
| **Pure White** | `#FFFFFF` | `rgb(255, 255, 255)` | Light canvas, card surfaces, primary text on dark. |
| **Slate Gray Light** | `#F8FAFC` | `rgb(248, 250, 252)` | Alternating rows, certificate parchment background. |

### Mythos Brand Spectrum (Accents & Highlights)
| Color Name | HEX | RGB | Primary Function |
| :--- | :--- | :--- | :--- |
| **Electric Blue** | `#2563EB` | `rgb(37, 99, 235)` | Primary CTAs, active pills, links, certificate primary accents. |
| **Royal Blue** | `#1E3A8A` | `rgb(30, 58, 138)` | Outer certificate border, hero dark glows. |
| **Cyan** | `#06B6D4` | `rgb(6, 182, 212)` | Code highlights, secondary gradients, technical pills. |
| **Violet / Purple** | `#7C3AED` | `rgb(124, 58, 237)` | Data warehouse & modeling track, gradient middle stop. |
| **Magenta** | `#EC4899` | `rgb(236, 72, 153)` | Subtle decorative gradients, creative sparks. |
| **Split Orange** | `#F97316` | `rgb(249, 115, 22)` | Split 'O' in MYTHOS logo, schedule highlights, certificate seal. |
| **Emerald Green** | `#10B981` | `rgb(16, 185, 129)` | Verified status dots, WhatsApp buttons, success confirmation. |

---

## 4. Logo Usage, Asset Directory & Vector Geometry

### Official Brand Emblem Geometry:
* **The 'M' Ribbon**: Continuous 3D gradient ribbon sculpture forming the letter **'M'**.
  - **Left Pillar**: Electric Blue (`#2563EB`) & Cyan (`#06B6D4`) rounded column symbolizing foundational stability and code extraction.
  - **Valley Center**: Floating `< / >` code symbol in indigo and orange nestled in the upper notch.
  - **Center Fold**: Indigo (`#4F46E5`), Violet (`#9333EA`), and Magenta (`#EC4899`) transition representing data pipeline transformation.
  - **Right Pillar & Arrow**: Rises into a 45-degree ascending arrow in Vivid Orange (`#F97316`) and Amber (`#FB923C`) symbolizing upward career trajectory and executive mastery.
  - **Digital Voxels / Pixels**: Floating 3D cubes / pixels dispersing into the upper right representing modern digital ecosystems, cloud infrastructure, and data scale.

### High-Resolution Asset Master Catalog:

| File Name | Location | Format & Resolution | Purpose & Usage |
| :--- | :--- | :--- | :--- |
| **`mythos_icon_transparent.png`** | `design/assets/` & `app/static/Images/mythos/` | PNG (1024x1024 RGBA) | Zero-halo unmultiplied transparent icon for headers, navbars, and cards. |
| **`mythos_icon_2048.png`** | `design/assets/` | PNG (2048x2048 RGBA) | Ultra-HD master print icon for brochures, certificates, and billboards. |
| **`mythos_icon.jpg`** | `app/static/Images/mythos/` | JPEG (1024x1024 RGB) | Crisp high-resolution icon master on clean white backdrop. |
| **`mythos_full_transparent.png`** | `design/assets/` & `app/static/Images/mythos/` | PNG (1376x768 RGBA) | Complete transparent horizontal brand lockup (Emblem + Wordmark + Tagline + 5 Pillars). |
| **`mythos_full_logo.jpg`** | `app/static/Images/mythos/` | JPEG (1376x768 RGB) | Master full-color corporate brand board on solid white canvas. |
| **`mythos_logo_dark.jpg`** | `design/assets/` & `app/static/Images/mythos/` | JPEG (1376x768 RGB) | Dark-mode glowing neon brand render on Deep Navy (`#070B14`). |
| **`hero_art.jpg`** | `app/static/Images/mythos/` | JPEG (1376x768 RGB) | 3D Hero artwork: 'M' ribbon on illuminated neon podium with digital wireframe globe. |
| **`hero_podium.jpg`** | `app/static/Images/mythos/` | JPEG (1376x768 RGB) | 3D Hero podium master asset for platform landing showcase. |
| **`mythos_emblem.svg`** | `design/assets/` & `app/static/Images/mythos/` | SVG Vector (512x512) | Scalable vector graphic of the official 3D 'M' ribbon and voxels. |
| **`mythos_icon.svg`** | `design/assets/` | SVG Vector (512x512) | Radial aperture gear vector icon for seal and technical stamps. |
| **`mythos_logo.svg`** | `design/assets/` | SVG Vector (600x120) | Scalable horizontal vector lockup with split 'O' wordmark. |

### Construction Rules:
* **Minimum Clear Space**: Maintain at least `1x` the height of the 'M' as padding around the entire logo.
* **Prohibited Modifications**:
  - Do not alter the split colors of the 'O' (always Blue on left, Orange on right).
  - Do not stretch, distort, or rotate the logo off-axis.
  - When placing on light backgrounds, use Dark Navy `#0F172A` text; when on dark backgrounds, use Pure White `#FFFFFF`.

---

## 5. Official Certificate Generation Guidelines

These rules dictate the visual design, typography, dimensions, and dynamic fields when producing official **Certificates of Completion & Excellence** for graduating cohort students.

### Dimensions & Layout:
* **Standard Size**: **A4 Landscape** (`297mm x 210mm` / `11.69" x 8.27"`).
* **Digital Resolution**: `3508 x 2480 pixels` at **300 DPI**.
* **Orientation**: Strictly Landscape.
* **Safe Margin**: Minimum `20mm` (approx. 236px) inset from every edge.

### Border & Guilloche Framework:
* **Outer Frame**: Double-line border with rounded corner flourishes:
  - Outer primary rule: `6pt` width in **Royal Blue** (`#1E3A8A`).
  - Inner decorative accent rule: `1.5pt` width in **Electric Blue** (`#2563EB`) separated by `4mm` white gap.
  - Four Corner Cornerstones: Minimalist L-bracket or 45-degree angled chevron in **Vivid Orange** (`#F97316`).

### Certificate Element Hierarchy:
1. **Institution Logo & Wordmark**:
   - Centered at the top: Mythos Icon (`48px` diameter) with `MYTHOS` wordmark.
   - Subtitle: `ACADEMY OF DATA SYSTEMS & ARCHITECTURE`.
2. **Certificate Header**:
   - `CERTIFICATE OF EXCELLENCE & COMPLETION`
   - Font: Poppins SemiBold, `16pt`, tracking `3pt`, color `#2563EB`.
3. **Attribution Prefix**:
   - `THIS IS PROUDLY PRESENTED TO`
   - Font: Poppins Regular, `10pt`, tracking `2pt`, color `#64748B`.
4. **Candidate Full Name**:
   - Dynamic Student Name: (e.g. `PRIYA VERMA` or `ROHAN SHARMA`)
   - Font: Poppins Bold, `34pt`, color `#0F172A`.
   - Subtle decorative gradient underline (`#2563EB` to `#F97316`, `3pt` thick, `140mm` width).
5. **Certification Statement**:
   - `For successfully completing the comprehensive 10-week intensive mentorship program and demonstrating rigorous practical capability in building production-grade analytical data systems.`
   - Font: Poppins Regular, `11pt`, color `#475569`, line spacing `1.6`.
6. **5 Accredited Pillars (Badge Strip)**:
   - Centered horizontal strip of 5 tool badges:
     `[ Python ETL ]   [ Relational SQL ]   [ Power BI ]   [ Advanced Excel ]   [ Tableau ]`
7. **Official Security & Verification Footer**:
   - **Left**: Date of Issue (e.g. `November 12, 2026`) and Cohort Code (e.g. `Batch: DA-WKND-2026-B1`).
   - **Center**: Official Mythos Golden Embossed Digital Seal (`VERIFIED & ACCREDITED MENTORSHIP`).
   - **Right**: Unique Serial ID & Verification Link:
     - `Certificate ID: MYTHOS-DA-2026-B1042`
     - QR Code linking to `https://mythostech.in/verify/{CERT_ID}`.
8. **Signatures**:
   - **Lead Technical Mentor**: Data Architecture & Analytics
   - **Program Director**: Admissions & Cohort Management

---

## 6. How to Generate Certificates Programmatically

A complete, self-contained Python generator script is provided in this directory:
`design/certificate_generator_template.py`

### Running the Generator:
```bash
python design/certificate_generator_template.py --name "Priya Verma" --id "MYTHOS-DA-2026-B1001"
```
The script reads `design/tokens.json`, builds the vector elements, renders high-res Poppins typography, and outputs a print-ready PDF and 300-DPI PNG in `app/static/certificates/`.
