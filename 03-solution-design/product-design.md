# Product Design — Iris (Curriculum Skill Alignment)

> Rewritten 2026-08-27 for the national-standard pivot and the two-surface deployment.
> Supersedes the 2026-04-30 design, which assumed a single application serving
> administrators, curriculum designers, and students against a self-built vocabulary.

---

## Product Vision

Give a Thai curriculum committee an evidence-based answer, in the state's own skill
vocabulary, to two questions they currently answer from opinion:

1. **Which skills that our graduates' target careers demand does this curriculum not
   develop?**
2. **For the skills that become more central as that career progresses — how deeply does
   this curriculum develop them?**

The second question is answerable because the standard pairs 13 digital careers by
seniority. It is *not* a question about a proficiency level the market requires; no such
figure exists.

---

## Two surfaces, deliberately different

| | Public | Gated |
|---|---|---|
| **Route** | `vru-ai.com/iris` | `vru-ai.com/iris/app` |
| **Who** | Anyone — colleagues, reviewers, other departments, prospective students | Department faculty only, via Cloudflare Access |
| **Can** | Read published analyses, understand the method and its limits | Upload มคอ.2, run analyses, review and correct links, publish |
| **Depends on the engine** | No — build-time JSON | Yes — Cloudflare Tunnel to `linux-gpu-server` |

The public surface is a **research showcase**: it must be readable, citable, and honest
about what the data does and does not support. The gated surface is a **working tool**
for a handful of known users; density beats polish there.

---

## Personas

### Ajarn Somchai — Curriculum Committee Member *(primary, gated)*
- **Role:** Lecturer serving on the CS curriculum revision committee
- **Goal:** Enter the revision meeting with evidence instead of anecdote — which skills
  are missing, which are shallow, which courses would have to change
- **Pain:** Revision discussions are opinion-driven; comparisons with other universities
  are impressionistic; TQF documents are 200 pages nobody reads end to end
- **Technical proficiency:** Comfortable with the domain, not with data tools. Will not
  open a terminal
- **Context:** Revision cycle, a few intense weeks every few years
- **Needs from Iris:** to *disagree with it productively* — see why a skill was assigned,
  and correct it when it is wrong

### Ajarn Malee — Department Head *(secondary, gated + public)*
- **Role:** Head of department, answerable to faculty leadership and accreditation
- **Goal:** Show that curriculum decisions are evidence-based and aligned with the
  national standard the ministry itself publishes
- **Pain:** Cannot currently produce that evidence
- **Context:** Accreditation preparation, faculty reporting, benchmarking against peers
- **Needs from Iris:** an exportable report, and a public page she can point people to

### A visiting reader *(public)*
- Another department's lecturer, a reviewer, a researcher, a student
- **Goal:** understand what this project found and whether the method is sound
- **Needs:** the method explained, the limitations stated up front, results legible
  without an account, a PDF to take away

*Removed:* the student/career-advisor persona from the previous design. It implied
individual-level advice that programme-level analysis cannot support, and no student
stakeholder was available to validate it. If it returns, it needs its own research
question.

---

## The journey that matters most

**Ingest → review → analyse → publish.** The review step is the one the previous design
did not have, and it is the one that makes the tool trustworthy.

```
1. UPLOAD        Somchai uploads มคอ.2 (PDF)
                 └─ integrity gate runs immediately
                    ✓ clean          → continue
                    ⚠ repairable     → "tone marks were damaged and restored" + sample
                    ✗ unusable       → refuse, explain the defect, ask for a better file

2. EXTRACT       78 courses found, each showing its source page
                 └─ he spot-checks three against the PDF

3. LINK          each course gets skills at a level, with the evidence span highlighted
                 └─ ⏱ this takes minutes, not seconds — progress must be honest

4. REVIEW        ◄── the critical screen
                 he works down the low-confidence links: accept, reject, adjust level
                 disagreements between level sources are surfaced, not hidden

5. ANALYSE       he picks a career (e.g. วิศวกรข้อมูล) and gets a prevalence-ranked gap,
                 plus — since that career is seniority-paired — which skills matter more
                 at senior level and how deeply the curriculum develops them

6. PUBLISH       Malee reviews and promotes it to the public site
```

---

## Features

| # | Feature | Surface | Sprint | Priority |
|---|---|---|---|---|
| F1 | Upload มคอ.2 with an integrity verdict | Gated | 9 | Must |
| F2 | Course list with source-page provenance | Gated | 9 | Must |
| F3 | **Skill-link review — accept / reject / adjust level** | Gated | 9 | **Must** |
| F4 | Career selector across 138 digital careers | Both | 8/9 | Must |
| F5 | Alignment report — prevalence-weighted ranked gaps | Both | 8 | Must |
| F6 | Courses × skills heatmap, level-shaded | Both | 8 | Must |
| F7 | Narrative summary | Both | 8 | Must |
| F8 | PDF export | Both | 8 | Must |
| F9 | Programme-to-programme comparison | Both | 8 | Must |
| F10 | Method and limitations page | Public | 8 | Must |
| F11 | Curriculum revision scenario | Gated | 9 | Should |
| F12 | Growth-adjusted view (`skillsGrowth`) | Both | 8 | Should |
| F12b | Seniority-gradient panel (13 paired careers) | Both | 8 | Should |
| F13 | Publish / unpublish an analysis | Gated | 9 | Should |
| F14 | Skills found that the standard lacks | Gated | 9 | Could |

---

## Screens

### Public

| Screen | Contents |
|---|---|
| **Project overview** | What Iris does, why the national standard matters, method summary, **limitations stated up front** — not buried |
| **Published analyses** | Cards: programme, career, date, snapshot version |
| **Alignment report** | Heatmap · ranked gap table (prevalence-weighted) · **seniority-gradient panel** where the career is paired · narrative · PDF download · snapshot and model provenance footer |
| **Programme comparison** | Two profiles side by side: shared, A-only, B-only, different-level |
| **Method** | Ingestion, linking, level inference, metrics; annotation protocol and agreement figures |

### Gated

| Screen | Contents |
|---|---|
| **Programme library** | Ingested programmes, status, last analysed |
| **Upload** | Drop zone → integrity verdict → extraction progress |
| **Course review** | Extracted courses; click through to the source page |
| **Skill-link review** | **The core working screen** — see below |
| **Run analysis** | Career picker, scenario options, run |
| **Analysis result** | As the public report, plus per-link confidence and edit affordances |
| **Publish** | Preview the public view, confirm, promote |

### The skill-link review screen

This screen carries the product. An LLM proposing skill assignments that nobody can
inspect is not evidence — it is a black box wearing a lab coat.

Each row shows:

- the **skill** (Thai + English) and its official definition
- the **assigned level**, with the criteria for that level from the standard
- the **evidence span** highlighted inside the course description
- **level-source agreement** — CLO / curriculum map ● ○ / curriculum position, and where
  they disagree
- **confidence**, including whether the Thai and English channels agreed
- actions: accept · reject · change level

Default ordering is **lowest confidence first**, so limited attention goes where it
changes outcomes. Bulk-accept high-confidence links so review is finishable in one
sitting.

---

## Information architecture

```
vru-ai.com/iris                        overview
├── /analyses                          published list
│   └── /:programme/:career            report
├── /compare/:a/:b                     comparison
├── /method                            method + limitations
└── /app                    🔒 Cloudflare Access
    ├── /programmes                    library
    │   └── /:id
    │       ├── /courses               extracted courses
    │       └── /links                 skill-link review
    ├── /upload
    └── /analyses/:id
```

---

## Interface principles

**1. Never overstate what the data contains.** Two hard limits, both enforced in the
narrative template rather than left to the writer:

- **Truncation.** The demand vector is capped at ~100 skills per career. The interface may
  say *"not in the top-100 demanded for this career"*; never *"the market does not demand
  this."*
- **No demand-side level.** The standard publishes no required proficiency level per
  career × skill. Level is a property of the *curriculum* — "this programme develops SQL
  to advanced level" is sayable; "the market requires intermediate SQL" is not. Where the
  interface shows depth against demand, it shows the **seniority gradient** (which skills
  gain prominence from Data Scientist to Senior Data Scientist), labelled as such.

**2. Provenance is always one click away.** Every skill traces to a course; every course
traces to a page in the source PDF. Committee members will challenge specific
assignments, and being able to answer immediately is what earns the tool a place in the
meeting.

**3. Show disagreement.** Where level-inference sources conflict, show the conflict.
A tool that hides its uncertainty gets trusted once and abandoned after the first
confident error.

**4. Honest progress.** Linking 78 courses through a local LLM takes minutes. Show
courses completed, not a spinner, and let the user leave and come back.

**5. Thai first.** Thai UI with English secondary. Thai typography needs real attention —
line height for stacked diacritics, a font that renders tone marks correctly. The whole
feasibility study is a lesson in what happens when Thai text handling is an afterthought.

---

## Design system

| Concern | Choice |
|---|---|
| Framework | Astro — static pages, islands for heatmap, review table, comparison |
| Typography | Thai-first stack (Sarabun or IBM Plex Sans Thai); verify tone-mark and karan rendering at every weight |
| Palette | Restrained academic neutrals; colour reserved for the level scale and gap severity |
| Level scale | Three steps, ordinal, distinguishable without colour (pattern or label too) |
| Heatmap | Custom island; courses × skills, shaded by level, gap severity by intensity |
| Charts | Client-side island, no runtime dependency for the static shell |
| Accessibility | WCAG 2.1 AA; never colour alone for level or severity |
| Language | Thai primary, English secondary; skill labels always available in both |

---

## Success measures

| Measure | Target | How |
|---|---|---|
| Review completion | A committee member finishes reviewing a 78-course programme in one sitting (< 90 min) | Timed session with two faculty |
| Correction rate | Proportion of links edited during review — tracks against the Sprint 4 evaluation figures | Instrumented |
| Provenance use | Committee members follow a link back to the source page at least once per session | Instrumented |
| Report comprehension | ≥ 4 of 5 faculty correctly identify the top three prevalence-weighted gaps unaided, **and none reads the seniority panel as a required proficiency level** | Usability session |
| Meeting adoption | The report is cited in an actual curriculum revision meeting | Observation |
| Public legibility | A reader outside the department can state one correct limitation after reading the overview | Informal review |

*Removed:* the previous design's "< 5 minutes from upload to report" target. Linking a
216-page document through a local LLM will not meet it, and the honest response is to
design for a wait rather than to promise a speed the method cannot deliver.

---

_Phase 3 is complete when this design, the solution proposal, and the data feasibility
study agree with one another, and Sprint 0 can begin._
