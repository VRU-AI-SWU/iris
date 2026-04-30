# Product Design — Iris (Skill Gap Analysis)

---

## Product Vision

Iris gives Thai academic administrators and curriculum designers a clear, evidence-based picture of how their programme's skill profile compares to other programmes and to current job market demand — so they can make confident, data-driven curriculum decisions.

---

## User Personas

### Persona 1: Araya — Academic Administrator
- **Role:** Head of Department, Computer Science, mid-sized Thai university
- **Goals:** Demonstrate programme quality to accreditation bodies; identify which skills are underrepresented before the next curriculum review cycle; benchmark against competitor programmes
- **Pain points:** No objective tool for cross-programme comparison; curriculum review discussions are opinion-driven; accreditation requires evidence she currently cannot produce
- **Technical proficiency:** Low — comfortable with Excel and PowerPoint, not with data science tools
- **Usage context:** Quarterly review meetings; accreditation preparation; responds to institutional pressure to modernise the curriculum

### Persona 2: Krit — Curriculum Designer
- **Role:** Senior Lecturer responsible for curriculum development
- **Goals:** Know exactly which courses are contributing which skills; identify specific courses to update when a gap is identified; plan elective bundles that address market gaps
- **Pain points:** No visibility into how course descriptions map to skill outcomes; changes to one course's contribution are invisible at the programme level
- **Technical proficiency:** Medium — can interpret charts and tables; not a data scientist
- **Usage context:** Between semesters; when planning new courses or revising existing ones

### Persona 3: Nok — Student / Career Advisor
- **Role:** Final-year CS student (or career advisor at the university careers centre)
- **Goals:** Understand whether their programme prepares them for a specific career path; identify personal skill gaps to address before graduation
- **Pain points:** No transparent view of what the programme covers relative to job requirements; career advisor guidance is anecdotal
- **Technical proficiency:** Low to medium
- **Usage context:** Career planning sessions; when considering postgraduate study or job applications

---

## User Journey Map

_Primary persona: Araya (Academic Administrator)_

| Stage | User Action | User Feeling | System Response | Opportunity |
|---|---|---|---|---|
| Awareness | Hears about Iris from a colleague at another university | Curious, slightly sceptical | — | Clear one-page explainer on landing page |
| Onboarding | Uploads her department's TQF PDF | Uncertain — "will it understand Thai?" | Confirms upload, runs extraction, shows parsed course list for review | Show parsed course list immediately so she can verify accuracy |
| Core use — Market gap | Selects "Data Engineer" career path; requests gap report | Engaged, cautious | Displays heatmap, narrative summary, ranked gap table | Narrative summary must be non-technical and actionable |
| Core use — Comparison | Compares her programme against a competitor university's programme | Competitive interest | Side-by-side skill decomposition; common vs. unique skills | Highlight differences that matter most (RCA-weighted) |
| Scenario planning | Asks "what if we add these electives?" | Empowered | Scenario view: before/after skill distribution and gap scores | Make scenario builder self-explanatory with guided UI |
| Report export | Exports PDF report for department meeting | Relieved | Clean formatted PDF with heatmap and narrative | One-click export; report must be presentation-ready |
| Return | Returns next semester after curriculum changes | Invested | Re-runs analysis on updated TQF; comparison against previous run shows improvement | Support version comparison over time |

---

## Feature List

| Feature | User Story | Priority | Persona |
|---|---|---|---|
| TQF document upload and parsing | As an administrator, I want to upload a TQF PDF so that the system can extract my programme's course structure | Must | Araya |
| Skill extraction and vocabulary display | As an administrator, I want to review the skills extracted from my courses before analysis so that I can trust the results | Must | Araya, Krit |
| Programme-to-market gap report | As an administrator, I want to see a gap report between my programme and a target career path so that I know which skills are missing | Must | Araya |
| Heatmap (courses × skills) | As a curriculum designer, I want to see which courses contribute which skills so that I know which courses to update | Must | Krit |
| Narrative summary | As an administrator, I want a plain-language summary of the gap analysis so that I can share it with colleagues who won't read charts | Must | Araya |
| Ranked gap table (RCA-weighted) | As an administrator, I want a prioritised list of skill gaps so that I know where to focus curriculum changes first | Must | Araya, Krit |
| Programme-to-programme comparison | As an administrator, I want to compare two programmes side-by-side so that I can differentiate my programme or identify overlap | Must | Araya |
| Career path taxonomy (20-role) | As a student, I want to select a career path from a list so that I can see how my programme aligns with that specific role | Must | Nok |
| PDF report export | As an administrator, I want to export a formatted PDF report so that I can present findings in department meetings | Must | Araya |
| Scenario builder | As a curriculum designer, I want to add or remove courses from a hypothetical scenario so that I can see the skill impact before committing to changes | Should | Krit |
| Course drill-down view | As a curriculum designer, I want to click on a skill in the heatmap to see which courses cover it and at what weight | Should | Krit |
| Programme library | As a user, I want a library of uploaded programmes so that I can quickly select programmes for comparison without re-uploading | Should | Araya |
| Version comparison | As a curriculum designer, I want to compare the current programme against a previous version so that I can quantify the impact of changes already made | Should | Krit |
| ESCO skill mapping view | As a researcher, I want to see how extracted skills map to ESCO taxonomy codes so that I can report findings in an internationally comparable format | Could | Araya (for accreditation) |
| Job posting sample view | As an administrator, I want to see sample job postings that contributed to the market distribution so that I can understand what employers are actually asking for | Could | Araya |
| Student career alignment view | As a student, I want to enter my enrolled programme and a target job role to see my skill gap and what I should learn | Could | Nok |

---

## Screen / View Inventory

| Screen | Purpose | Key Actions |
|---|---|---|
| Landing / Home | Entry point; explains Iris and routes to main features | Navigate to Programme Library, Start New Analysis |
| Programme Library | Browse and manage uploaded programmes | Upload new TQF PDF, Select programme, Delete programme |
| Programme Profile | View extracted skill distribution for a single programme; shows course list, credit allocation, and skill heatmap | Edit course weights, Drill into course, Start gap analysis |
| Programme-to-Market Gap Report | Main output view: heatmap, ranked gap table, narrative summary for a programme vs. a career path | Select career path, Switch scenario, Export PDF |
| Programme-to-Programme Comparison | Side-by-side skill decomposition for two programmes | Select second programme, View common / A-unique / B-unique skills |
| Course Drill-Down | Skill contribution view for a single course | View skills extracted from this course, See weight contribution |
| Scenario Builder | Add/remove courses and see live skill distribution and gap score changes | Toggle courses, Add hypothetical course, Save scenario, Compare to base |
| Career Path Selector | Browse the 20-role Thai digital taxonomy with role descriptions | Select role, View market demand distribution |
| Report Export | Preview and download formatted PDF report | Select report sections, Download |
| Admin: Job Posting Dataset | View and manage the job posting dataset (collection date, platform, career path coverage) | View dataset stats, Trigger re-collection (v2) |

---

## Navigation & Information Architecture

```
Iris
├── Home
├── Programmes
│   ├── Programme Library
│   │   └── [Programme Card] → Programme Profile
│   │       ├── Course List
│   │       ├── Skill Heatmap (courses × skills)
│   │       └── Course Drill-Down
│   └── Upload New TQF
├── Analyse
│   ├── Programme vs. Market
│   │   ├── Select Programme
│   │   ├── Select Career Path (20-role taxonomy)
│   │   ├── Select Scenario (Core / +Electives / Hypothetical)
│   │   └── Gap Report View
│   │       ├── Heatmap
│   │       ├── Ranked Gap Table
│   │       ├── Narrative Summary
│   │       └── Export PDF
│   └── Programme vs. Programme
│       ├── Select Programme A
│       ├── Select Programme B
│       └── Comparison View
│           ├── Common Skills
│           ├── A-Unique Skills
│           └── B-Unique Skills
├── Scenarios
│   ├── Scenario List
│   └── Scenario Builder
│       ├── Base Programme
│       ├── Toggle Courses
│       └── Before / After View
└── Settings
    ├── Job Posting Dataset
    └── Skill Vocabulary
```

---

## Wireframe Notes

_Full wireframes to be produced by UX/UI Designer in Phase 3. Key layout decisions documented here._

**Programme-to-Market Gap Report (primary screen):**
- Top: Programme name + career path name + scenario selector + export button
- Left panel (60%): Heatmap — rows = courses, columns = top-N skills, colour intensity = skill weight; cells are clickable (→ course drill-down)
- Right panel (40%): Ranked gap table (skill name, gap score, RCA weight, missing/partial indicator) + narrative summary paragraph below
- Below fold: Aggregate KL divergence score with plain-language interpretation ("Your programme covers X% of the skills demanded for this career path")

**Scenario Builder:**
- Split view: current distribution (left) and scenario distribution (right)
- Course checklist with toggle switches; hypothetical course name entry field
- Gap score delta shown live as courses are toggled

**Programme-to-Programme Comparison:**
- Three columns: A-unique | Common | B-unique
- Skill chips in each column, sized by weight
- Summary row at top: overall cosine similarity score

---

## Design System Notes

- **Typeface:** System sans-serif stack (Inter preferred); Thai character support required — verify rendering
- **Primary colour:** To be defined by UX/UI Designer; suggest neutral academic palette (avoid consumer-app vibrancy)
- **Component library:** shadcn/ui (React, Tailwind-based) — well-suited for data-dense admin interfaces
- **Heatmap library:** Recharts or D3.js — D3 preferred for custom heatmap control
- **Accessibility standard:** WCAG 2.1 AA minimum; Thai language screen reader support is secondary (academic admin context)
- **Language:** Thai UI primary; English secondary (toggle or bilingual labels)

---

## Metrics (UX)

| Metric | Target | Measurement Method |
|---|---|---|
| Time-to-first-gap-report (from TQF upload) | < 5 minutes | Instrumented timer from upload completion to report display |
| Administrator comprehension of heatmap | ≥ 80% correctly interpret top-3 gap skills without assistance | Usability test with 5 academic administrator participants |
| Narrative summary usefulness rating | ≥ 4/5 in user survey | Post-session questionnaire |
| Report export adoption | ≥ 60% of sessions that complete a gap report also export PDF | Analytics event tracking |
| Scenario builder adoption | ≥ 30% of returning curriculum designer sessions use scenario builder | Analytics event tracking |

---

_Phase complete when: All screens are wireframed, user stories have acceptance criteria, and the development team can begin implementation._
