# Annotator Guideline — Linking Courses to the National Skill Standard

<!-- lang-switch -->
**English** · [ภาษาไทย](annotation-guideline.md)

**Project Iris · Sprint 4 (Evaluation Gate)**
Version 2026-08-31 · about 20 minutes to read the first time

> The Thai version is the one the annotators work from. This is a translation for the
> record and for readers outside the department.

---

## 1. What the task is

Read a **course description** from a TQF (มคอ.2) document and identify which of the
**4,376 skills** in the national skill vocabulary (สป.อว. / KMITL) that course
**develops**, together with the **proficiency level** it develops them to.

What you produce is the **gold standard** used to measure how well the automated system
performs. It is not a review of the system's work — **you will not see the system's output
at all until you have closed the first round.**

### Why two annotators, working separately

To measure *how far two experts agree*. If two faculty members cannot agree on what
skills a course develops, then no accuracy figure for the model means anything. This
agreement statistic is reported in the paper.

🔴 **Please do not consult each other during the first round.** If you get stuck, record
the question in the `notes` column and raise it in the adjudication round after both of
you have submitted.

---

## 2. Three rules that must not be broken

These are not arbitrary. Each comes from a real mistake made during the development round
(Sprint 3) — a mistake that made the measured precision figure **wrong enough to withdraw**.

### Rule 1 — read every phrase of the *course description*, not the course title

In the development round, the course `คพ231 Data Communications and Computer Networks` was
labelled with a single skill, *Computer Networking*, because the label was decided from the
title. But the description states plainly:

> …data communication architecture and protocols, **static and dynamic routing protocols**,
> access control, building networks with LAN switching equipment…

*Routing Protocols*, *Communication Protocols* and *Data Networks* are all in the
vocabulary, and the course develops all of them. **Omitting them caused a correct system
to be scored as wrong.**

**In practice:** read the description one phrase at a time, asking of each phrase,
*"does this say what a student will be able to do?"*

### Rule 2 — finish the labels **before** seeing the system's output

Widening a label set after seeing what the system answered turns a measurement into a
self-portrait. The second-round file is only released once the first round is complete.

### Rule 3 — a course may have **many** skills, and that is normal

There is no limit. A core course typically develops 3–8 skills. Do not pick the single
"best-fitting" skill — record every skill the description supports.

---

## 3. Steps for one course

1. **Read the whole description once** before searching the vocabulary.
2. **Underline each phrase** that states a capability — e.g. `relational database design`,
   `normalisation`, `SQL`.
3. **Search the vocabulary** for each phrase (Thai and English both work).
4. **Read the definition** of any skill you find before deciding — a skill's *name* can be
   ambiguous; its definition is not.
5. **Record the skill, the evidence text, and the level.**
6. Any phrase you cannot find in the vocabulary goes in the **out-of-vocabulary** column.
7. Finish every phrase before moving to the next course.

---

## 4. Deciding whether a course "develops" a skill

**The test:** on completing the course, a student **can do that thing** — not merely *has
heard of it*, and not merely *it belongs to the same field*.

| Situation | Include? |
|---|---|
| The description says it is taught / practised / designed / built | ✅ yes |
| Mentioned as context or as a passing example | ❌ no |
| A tool used in the course and named explicitly (e.g. `SQL`) | ✅ yes |
| In the same field, but the description does not mention it | ❌ no |
| A skill you must *already have* to take the course (a prerequisite) | ❌ no |
| A skill students "probably pick up" but that does not appear in the text | ❌ no |

⚠️ The last two rows are where two annotators most often diverge. When in doubt, follow
**what is actually written**, and record the hesitation in the notes column.

---

## 5. The evidence span

Every skill you record needs a phrase **copied from the course description** as evidence.

- **Copy it, do not rephrase it.** A curriculum committee will point at a skill and ask
  "where does the document say that?" The evidence has to point back into the document.
- Copy a short sufficient phrase; there is no need to quote a whole paragraph.
- One phrase can be evidence for several skills. But if you find yourself using **the same
  phrase for five or six skills**, go back and reconsider — that usually means the
  selection has gone too broad.

---

## 6. Skills the vocabulary does not contain

The vocabulary was built from labour-market data, so it names *what people at work do*
rather than *what universities teach*. Some courses genuinely develop skills the
vocabulary has no word for. This was measured on 2026-08-31: *Computer Architecture*,
*Discrete Mathematics* and *Cooperative Education* appear nowhere in the vocabulary, not
even inside a definition.

**Record these in the `out-of-vocabulary` column, in Thai, in your own words.** This
residue becomes a proposal back to สป.อว. and part of the paper's contribution.

⚠️ **But beware the case where the vocabulary has it under another name.** There is no
entry called *Software Engineering*, yet there are 46 related skills —
`Requirements Analysis`, `Software Validation`, `Software Documentation`,
`Software Quality Control` and so on. **In that case record the narrower skills; it is not
out-of-vocabulary.** Please search with narrower terms before concluding that something is
absent.

---

## 7. Courses that develop no skill at all

**This is a correct answer, not a failure.** General-education courses — Thai language,
physical education, ethics — may develop nothing that a labour-market vocabulary names.
Leave the row empty and note *no matching skill in the vocabulary*. The proportion of
such courses is a statistic we report.

**Do not add a token skill** just to avoid an empty row.

---

## 8. Proficiency level

Each skill in the vocabulary has three levels: **basic · intermediate · advanced**, and
each level carries **criteria written as observable capabilities**.

🔴 **Judge against the criteria the vocabulary states, not against how hard the course
feels.**

Example criteria for *Computer Networking*:

| Level | Criteria |
|---|---|
| Basic | Understands network concepts and basic terminology · can identify common devices such as routers and switches · can set up a simple LAN |
| Intermediate | Configures and manages network devices and protocols · troubleshoots common connectivity problems · understands and applies basic network security |
| Advanced | Designs and optimises complex network architectures · applies advanced security measures · manages large networks including WAN and cloud integration |

### Three signals that help

1. **The verb in the course's CLOs** — `อธิบาย` (explain) sits below `ประยุกต์ใช้` (apply),
   which sits below `ออกแบบ` (design) / `วิเคราะห์` (analyse).
2. **The curriculum responsibility matrix** (● primary / ○ secondary) — ● means the course
   carries that learning outcome as its main responsibility.
3. **Position in the curriculum** — year-1 courses usually reach the basic level; year-4 and
   specialised electives usually reach higher.

### When the signals conflict

**Record the conflict; do not smooth it over.** Enter the level you judge best, then note
in the notes column which signal pointed where. How often the signals conflict is itself
one of this project's research findings.

---

## 9. Damaged text

The text extracted from มคอ.2 files carries **residual damage in its text layer** — some
tone marks and *karan* have become spaces or other characters. For example:

| What you see | What it should be |
|---|---|
| `เครือข ายคอมพิวเตอร=` | เครือข่ายคอมพิวเตอร์ |
| `วิเคราะห์และออกแบบระบบเครือข ายได2` | วิเคราะห์และออกแบบระบบเครือข่ายได้ |
| `การโปรแกรมฝ‚”งไคลเอนต=` | การโปรแกรมฝั่งไคลเอนต์ |

**Read through the damage as normal** — we deliberately do not repair this class of damage,
because guessing a tone mark can change the meaning (`ไม` and `ไม่` are different words).
If a passage is genuinely unreadable, **note it rather than guessing**.

---

## 10. A worked example

### `คพ231 Data Communications and Computer Networks`

> Principles of data communication, basic components of a data communication system,
> computer networks, data communication architecture and protocols, static and dynamic
> routing protocols, access control, building networks with LAN switching equipment…

| Skill | Evidence | Level | Reasoning |
|---|---|---|---|
| Computer Networking | `เครือข่ายคอมพิวเตอร์` | intermediate | The CLOs say `analyse and design`, but the content stops at configuring and building networks — it does not reach WAN or cloud |
| Routing Protocols | `โปรโตคอลการหาเส้นทางแบบสถิตและพลวัต` | intermediate | Naming both static and dynamic implies configuration |
| Communication Protocols | `สถาปัตยกรรมการสื่อสารข้อมูลและโปรโตคอล` | intermediate | |
| Network Architecture | `สถาปัตยกรรมการสื่อสารข้อมูล` | basic | Architecture is mentioned, but students are not asked to design one |

**The level signals available for this course:** CLOs = `อธิบาย` (understand),
`ประยุกต์ใช้…ออกแบบ` (apply), `วิเคราะห์และออกแบบ` (analyse) · responsibility matrix = ● at
1.1, 1.4, 2.2, 2.3, 3.1, 3.2, 3.4, 4.1, 5.2 · position = year 2.

⚠️ Note that this example yields **four skills** where the development round recorded one.
That is Rule 1 in practice.

---

## 11. What not to do

- ❌ Consult each other during the first round
- ❌ Decide from the course title instead of the description
- ❌ Add a skill students "probably get" that is not in the text
- ❌ Rephrase the evidence instead of copying it
- ❌ Add a token skill so a course is not left empty
- ❌ Change a label after seeing the system's output
- ❌ Judge level by how hard the course feels rather than by the vocabulary's criteria

---

## 12. The second round — reviewing the system's output

Once both of you have submitted the first round, a second file is released: **the system's
raw output**, with skill definitions, evidence spans, levels and confidence scores. The
task is to **accept / reject / correct** each one.

This round measures something different from the first: whether *having a person review
the system's output actually improves it*, and *how fast that review goes*. There is
research showing that a human plus a system can perform **worse** than the system alone,
through automation bias — so it has to be measured, not assumed.

**Please time your work** (or let the tool time it). Decisions per hour is the figure used
to design the review screen in Sprint 9.

---

## 13. Scope of the work

- **~50 courses**, stratified: core / elective / general education
- **2 annotators**, working the same set independently
- First round roughly **3–4 hours** each · second round roughly **1.5–2 hours**
- After both submit: a joint adjudication round of about 1 hour

**Questions that come up while working** go in the notes column — do not stop and wait for
an answer.
