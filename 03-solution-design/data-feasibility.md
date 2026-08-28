# Data Feasibility Study — Iris (post-pivot)

> Empirical groundwork for the Phase 3 redesign, run 2026-08-27.
> Two questions had to be answered with real data before any architecture could be
> chosen: (1) what does the national Skill Mapping standard actually give us, and
> (2) can we get clean structured text out of real TQF (มคอ.2) documents.

---

## Part 1 — The national skill standard

### Source and standing

| Item | Value |
|---|---|
| API | `https://api.skillmapping.in.th` (v0.8.1-beta-public) |
| Docs | `https://api.skillmapping.in.th/docs` (Scalar; spec at `/docs/json`) |
| Public portals | [skillmapping.in.th](https://www.skillmapping.in.th/en) · [skill-mapping.ops.go.th](https://skill-mapping.ops.go.th/) · [skill.kmitl.ac.th](https://skill.kmitl.ac.th/) |
| Operator | Office of the Permanent Secretary, MHESI (สป.อว.) |
| Originator | KMITL — initiated by Prof. Dr. Surin Khomfoi |
| Auth | None required. Rejects requests without a `User-Agent` (HTTP 403) |

The platform defines itself as bridging a **Demand Side** (skills the labour market
requires) with a **Supply Side** (competencies curricula produce). Only the demand
side is published. **The supply side is the gap Iris fills.**

### Snapshot taken

`data/skillmapping/2026-08-27/` — 14 MB, mirrored by `fetch_snapshot.py` (stdlib only).

| Entity | Count | Notes |
|---|---|---|
| Industries | 5 | aviation-and-logistics, robotic, **digital**, electric-vehicles, smart-electronics |
| Careers (digital) | 138 | v1 scope; 371 across all industries |
| Skills (vocabulary) | 4,376 | hard-skill 2,911 · tools 912 · soft-skill 553 |
| Skills referenced by digital careers | 2,043 | all mirrored with full detail |
| Career × skill demand pairs | 12,343 | median 92 skills per career |

Every one of the 2,043 skills carries a Thai `definition` and exactly **three
proficiency levels** (`ระดับพื้นฐาน` / `ระดับปานกลาง` / `ระดับสูง`), each with 3–5
explicit `criteria`. Bilingual coverage is complete: all 4,376 skills resolve under
`?locale=en` (only 63 are identical in both languages — proper nouns like `.NET Core`).

Example — `ภาษาไพธอน` / `Python` (type: tools):

| Level | First criterion |
|---|---|
| ระดับพื้นฐาน | เข้าใจไวยากรณ์พื้นฐานของ Python และประเภทข้อมูล |
| ระดับปานกลาง | สามารถใช้งานฟังก์ชัน โมดูล และการจัดการข้อผิดพลาดได้อย่างมีประสิทธิภาพ |
| ระดับสูง | สามารถออกแบบและพัฒนาแอปพลิเคชันและระบบ Python ที่ซับซ้อนได้ |

### What the demand figures actually mean

`percentage` is **prevalence, not a share**. Within any career, `count / percentage`
is constant, so `percentage = count / N × 100` where `N` is the number of postings
behind that career. Percentages therefore sum to far more than 100 (mean 1,358 %,
max 3,596 %).

**This matters for the gap metric.** KL divergence needs a probability distribution,
so using it requires renormalising to `p_i = count_i / Σ count_j` — a *different*
quantity ("share of all skill mentions") whose interpretation must be stated
explicitly. Prevalence is the more directly interpretable signal for a curriculum
committee: *"65 % of Data Engineer postings ask for SQL"* means something to an
administrator; *"SQL is 3.2 % of skill mentions"* does not.

### ⚠️ The demand side carries no proficiency level

Re-checked 2026-08-28. A career × skill entry contains exactly three fields:

```json
{ "skill": { "id": "...", "title": "ทักษะการวิเคราะห์", "type": "soft-skill", ... },
  "count": 49415, "percentage": 15.48 }
```

There is **no level, no seniority, no proficiency field** anywhere on the demand side. The
three graded levels belong to the *skill entity* — a general scale defining what
foundational / intermediate / advanced mean for that skill — not to what any career
requires.

**Consequence:** levels exist on the **curriculum side only**. Iris can report *"this
programme develops SQL to advanced level"*. It cannot report *"the market requires SQL at
intermediate level"*, because no such figure exists. Any metric defined as a shortfall
between a demanded level and a delivered level is uncomputable, and any sentence implying
one would be fabricated.

### Seniority-paired careers — the demand-side depth signal that does exist

The digital industry contains **13 careers paired by seniority**, which supports a derived
depth measure:

| Ladder | Careers |
|---|---|
| base → senior → lead → chief | `data-scientist` (four rungs) |
| base → senior | `data-engineer`, `web-developer`, `developer`, `application-developer`, `sound-designer`, `frontend-developer`* |
| base → lead | `project-manager`, `animator` |
| junior → base | `software-engineer` |

\* `senior-frontend-developer` has only 5 skills — one of the degenerate careers; exclude.

The prevalence change between rungs is interpretable. Data Scientist → Senior Data
Scientist, over the 76 skills common to both:

| Δ prevalence | Skill |
|---|---|
| +12.67 pp | การสร้างแบบจำลองทำนาย (predictive modelling) |
| +12.02 pp | การประยุกต์ใช้การเรียนรู้ของเครื่อง (applied ML) |
| +10.56 pp | การวิเคราะห์เชิงทำนาย (predictive analytics) |
| +10.50 pp | การสร้างแบบจำลองทางคณิตศาสตร์ (mathematical modelling) |
| +10.49 pp | สถิติเชิงพหุ (multivariate statistics) |
| +2.24 pp | จาวา (Java) |
| +1.45 pp | การสร้างภาพข้อมูล (data visualisation) |
| −0.58 pp | ทักษะการวิเคราะห์ (analytical skills) |

The skills that gain are uniformly the deeper, more specialised ones; the skills that stay
flat are the general or tooling ones. This is a measured signal about **which skills gain
prominence with experience** — not a proficiency requirement, and it must not be reported
as one. Only 13 of 138 digital careers are paired, so the axis is available for some
targets and absent for others.

### Data-quality limits that must be disclosed

1. **The demand vector is truncated at ~100 skills per career.** Distribution peaks
   at 92–98, caps at exactly 100 (2 careers). A skill's absence from a career's list
   therefore does **not** mean the market does not want it — only that it fell below
   the cut-off. Any claim of the form "the market does not demand X" is unsupportable.
2. **`N` varies by four orders of magnitude** — from 203 postings
   (`information-technology-web-manager`) to 6,291,725 (`software-engineer`), median
   25,740. A figure of 6.3 M postings for one career is not plausible as a Thai-only,
   point-in-time count. **The underlying corpus is probably international and/or
   cumulative over years.** This must be clarified with สป.อว./KMITL before the
   methods section is written — it directly affects whether Iris can claim to measure
   *Thai* labour-market alignment.
3. **168 career×skill pairs (1.4 %) have `count = 0`** — a skill listed for a career
   with zero evidence. Includes obvious errors such as Python and Pandas at 0.00 % for
   `วิศวกรข้อมูล` (Data Engineer). These rows must be filtered.
4. **Three careers are effectively empty**: `security-solutions-architect` (0 skills),
   `character-modeler` (4), `senior-frontend-developer` (5). Exclude or flag.
5. **API is beta** (`0.8.1-beta-public`). The pinned snapshot is the reproducibility
   anchor; analyses must record the snapshot date.

### Bonus signal available

`skillsGrowth` gives a per-skill growth rate per career (median 85 entries per career,
10,815 values, range 0–706 %). This supports a question the previous design could not
answer from a single scrape: **is the curriculum keeping up with skills that are
growing?**

---

## Part 2 — Can we parse real TQF documents?

Two documents tested, both CS bachelor programmes, both revised 2565/2022.

| | SWU | KU |
|---|---|---|
| Pages | 216 | 28 |
| Size | 15 MB | 309 KB |
| Producer | Bullzip PDF Printer 11.8 | Microsoft Word 2013 |
| Thai font | THSarabunPSK, **WinAnsi** encoding | TH SarabunPSK, mixed WinAnsi / Identity-H |
| Completeness | Full — หมวดที่ 1–8 | **Excerpt only** — 3.1.1–3.1.5, truncated mid-list |
| Curriculum Mapping table | ✅ present (p. ~1867 of text) | ❌ absent |
| CLO / MLO / ELO per course | ✅ present (ชุดรายวิชา format) | ❌ absent |
| Course descriptions | ✅ Thai | ✅ Thai **+ English** |
| Distinct course codes found | 78 | 67 |

### Finding A — both text layers are damaged, in different ways

Thai is set in TH SarabunPSK under **WinAnsi encoding**, which has no Thai codepoints.
Marks that stack at the second level above a consonant fall into font-private glyph
slots with no `ToUnicode` entry, and extract as ASCII junk.

**Three independent extraction engines produce identical damage** — this is in the PDF,
not the extractor:

| Engine | Implementation | Thai marks per 1,000 Thai chars |
|---|---|---|
| poppler `pdftotext` | C++ | 134.5 |
| PyMuPDF / MuPDF | C | 134.5 |
| [xberg](https://github.com/xberg-io/xberg) 1.0.14 | Rust | 134.5 |
| *(KU, clean baseline)* | — | *171.0* |

All three return `ข-อมูลทั่วไป`, `ผลการเรียนรู2`, `ระบบฐานข2อมูล`. Since no reader can
recover a mapping the PDF does not contain, this closes the question of whether a better
extractor would help.

⚠️ **A finding with direct design consequences.** xberg reports `quality_score: 1.0` and
`extraction_method: native` on this document — a perfect score on text whose karan is 99 %
destroyed. Generic document-quality metrics do not model Thai diacritic integrity, so
xberg's own `VlmFallbackPolicy.on_low_quality` would **never fire** here and the damaged
text would pass silently into the pipeline. Any automatic OCR-fallback policy Iris uses
must be driven by the Thai-specific diagnostic below, not by a general quality score.

Damage rate per mark, measured against KU as a clean baseline (marks per 1,000 Thai
characters):

| Mark | KU | SWU | Retained | Verdict |
|---|---|---|---|---|
| ั ิ ี ึ ื ุ ู | 8–36 | 8–38 | 88–134 % | **intact** |
| ็ | 2.89 | 1.71 | 59 % | partial loss |
| ่ mai ek | 24.35 | 11.78 | 48 % | partial loss |
| ้ mai tho | 23.31 | 3.18 | **14 %** | severe |
| ์ karan | 18.17 | 0.11 | **1 %** | severe |

So: **vowel marks survive; tone marks and karan do not.** The result is text like
`ผลการเรียนรู2` (ผลการเรียนรู้), `ข-อมูลทั่วไป` (ข้อมูลทั่วไป), `วิเคราะห=`
(วิเคราะห์), `เป?น` (เป็น), `ป‚ญญา` (ปัญญา), `ฝEก` (ฝึก), `เป€าหมาย` (เป้าหมาย).

**The damage is substitution, not deletion.** The substitute glyphs are recoverable:

| Glyph | Count | Follows | Recovers to |
|---|---|---|---|
| `2` | 2,592 | ข, ู, ด, ช | ้ |
| `=` | 1,021 | ร, ต, ห, ณ | ์ |
| `‚` | 233 | ป, ฟ, ฝ | ั |
| `-` | 211 | ู, ข, ด, ร | ้ (variant) |
| `?` | 176 | ป only | ็ |
| `A` | 165 | น, ว, ม | ่ |
| `E`, `€`, `F`, `C`, `r`, `K`, … | ~250 | various | ึ, ้, … |

Totalling all marks per 1,000 Thai characters: KU 171.0, SWU 134.5, **SWU plus the
4,918 detected substitutions 171.4**. The near-exact match to the clean baseline
indicates that essentially nothing is lost — the marks are all still present, wearing
the wrong glyph. A deterministic repair table keyed on `(substitute, preceding char)`
should recover the text; the residual gap needs verification on a larger sample
before this is claimed as complete.

**KU has a different defect:** `ำ` (sara am, U+0E33) appears **zero times** in 22,177
Thai characters — every one has collapsed to `า` (`คำอธิบาย` → `คาอธิบาย`, `การทำให้`
→ `การทาให้`). Unlike the SWU case this *is* lossy: nothing distinguishes an original
`า` from a collapsed `ำ` without a lexicon. Restoration needs a Thai dictionary or LM
pass and will not be perfect.

**Implication:** an automated **text-layer integrity gate** is mandatory before any
document enters the pipeline. The mark-rate-per-1,000-Thai-characters statistic used
above is itself the diagnostic — cheap, deterministic, and it flags both failure modes.

### Finding B — the ELO signal for level inference exists (in SWU)

The SWU document contains **แผนที่แสดงการกระจายความรับผิดชอบมาตรฐานผลการเรียนรู้จากหลักสูตรสู่รายวิชา
(Curriculum Mapping)** with ● ความรับผิดชอบหลัก / ○ ความรับผิดชอบรอง per course ×
learning outcome, **and** per-course CLOs and per-module MLOs mapped to programme ELOs.

That is a depth signal the programme declares about itself under TQF regulation — a
far better basis for inferring `พื้นฐาน / ปานกลาง / สูง` than asking an LLM to guess
from a course description. Combined with year-of-study (derivable from the course
code) and prerequisite chains, it gives three independent evidence sources.

**But KU's excerpt does not contain it.** The full KU มคอ.2 must be obtained before
level-aware mapping can be evaluated on more than one programme.

### Finding C — English course descriptions are a free parallel channel

KU gives every course a bilingual description:

> `01418101 การใช้งานคอมพิวเตอร์ 1(0-2-1) / (Computer Applications)`
> องค์ประกอบของระบบคอมพิวเตอร์ ฮาร์ดแวร์ ซอฟต์แวร์ ระบบปฏิบัติการ …
> *Computer system, hardware, software, operating system, word processing, database and other application software.*

Since the national vocabulary is fully bilingual, the English description can be
matched directly against English skill titles — **bypassing Thai text damage entirely
for those courses**. SWU's descriptions are Thai-only (English appears only in course
titles), so this is a per-document opportunity, not a general solution. The linker
should use both channels where available and agree between them as a confidence signal.

---

## Consequences for the architecture

1. **Deterministic glyph repair handles the SWU failure mode** — auditable, free,
   reproducible, and preferred wherever the damage is substitution rather than deletion.
   ⚠️ **Corrected 2026-08-28:** the original conclusion "no OCR is required" was wrong as a
   general rule. KU's `ำ` collapse is genuinely lossy, and the literature round found a
   self-hostable Thai-tuned 3B vision model reaching **Levenshtein 0.04 on Thai government
   forms** ([[nonesung-2026-typhoon-ocr]]). The gate therefore has **three** outcomes —
   clean / repairable / lossy-or-unusable → vision re-extraction, flagged as vision-derived.
2. **A text-layer integrity gate is a first-class pipeline stage,** not an afterthought.
   Documents must be classified `clean / repairable / unusable` before ingestion.
3. **No general-purpose extraction engine solves this.** Evaluating a third engine
   (xberg — Rust core, 106 formats, seven OCR backends including a VLM one) returned
   byte-identical damage and a perfect quality score. It remains interesting as an *OCR
   orchestration layer* for the vision fallback — it has fallback chains, confidence
   thresholds, and layout/table models — but its table extraction inherits the same
   corruption on the native path (the page-58 curriculum map came back as a header
   fragment with the ● ○ marks absent, since they are Wingdings glyphs with no
   `ToUnicode`). Evaluate in Sprint 1; do not delegate the gate to it.
4. **PageIndex is the right tool for locating sections** across universities that
   paginate and format differently, and its page-range nodes give the per-fact
   provenance an academic report needs. It must be used to *locate* `3.1.5
   คำอธิบายรายวิชา` and the Curriculum Mapping table, after which the section is
   extracted **exhaustively** — Iris needs all ~78 courses, not the top-k most relevant.
5. **No vector database is needed.** The skill vocabulary is fixed at 4,376 entries;
   at 768 dimensions that is a 13 MB in-memory matrix and exact cosine similarity is
   microseconds. `pgvector` solved a problem — unbounded emergent skill clusters — that
   the pivot deleted.
6. **The gap metric needs re-derivation** from prevalence rather than assumed
   distributions, and every claim must respect the ~100-skill truncation.

## Open items requiring external input

- [ ] Obtain the **full KU มคอ.2** — the current file is an excerpt without the
      Curriculum Mapping table
- [ ] Clarify with สป.อว./KMITL **what corpus the demand counts come from** (Thai vs
      international, time window, whether `N` is cumulative) — blocks the methods section
- [ ] Confirm whether the ~100-skill cap per career is a display limit or a data limit,
      and whether the full demand vector can be obtained for research use
- [ ] Validate the glyph repair table against a third TQF document from a different
      producer before treating it as general
