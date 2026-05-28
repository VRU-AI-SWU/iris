---
type: question
owner: UX/UI Designer + Domain Expert
status: open
---

## Question
What visualisation format is most actionable for academic administrators and non-technical stakeholders?

## Why This Matters for Iris
The gap analysis is only useful if decision-makers can interpret and act on it. The wrong visualisation format — even with correct analysis — leads to inaction or misinterpretation.

## Initial Hypothesis
Radar charts for overall skill distribution comparison; ranked gap tables for actionable drill-down; industry segment heatmap for strategic fit view. This needs validation with the target audience.

## Papers Addressing This
- [[ahadi-2022-skills-taught-vs-sought]] — EDM 2022; heatmap (courses × occupations) with RCA weighting validated for academic stakeholders; unexpected pathway insights surfaced
- [[hilliger-2022-curriculum-analytics-tool]] — Journal of Computing in Higher Education 2022; multi-level reporting (student/course/program); managers 76/100, faculty 85/100; administrators harder to design for

## Current Working Answer
status: partial

**What the literature validates:**

1. **Heatmap (course × skill matrix)** — most effective single visualisation for academic stakeholders. Both ahadi-2022 and hilliger-2022 use it. Shows multi-course × multi-skill gap landscape in one view. Administrators and deans can see at a glance which courses cover which required skills.

2. **Multi-level output is mandatory** — administrators want programme-level summaries; department heads want course-level drill-down. Hilliger-2022 confirms: multi-level reporting is what turns a CA tool from a curiosity into a decision-support system.

3. **Lead with narrative, not charts** — administrators are harder to design for than faculty. Iris reports should lead with a plain-language headline ("Your programme is missing 3 of the top 10 skills required for Data Science") before any visualisations.

4. **Radar chart (optional)** — useful for 5–10 skill comparison between programme and market distribution. Validated in hilliger-2022 for competency attainment views. Not suitable for large skill sets (> 15 skills).

5. **RCA-weighted ranking table** — ranked list of skill gaps by RCA score (not raw frequency) surfaces the most career-path-specific missing skills first. Validates our earlier intuition that raw frequency over-represents generic skills.

**Revised visualisation plan for Iris:**
- **Primary output**: Heatmap (TQF courses × top-N required skills; cells = coverage status + gap magnitude)
- **Summary header**: Narrative gap summary (top 3–5 missing skills, overall alignment score)
- **Supplementary**: Ranked gap table (skill × gap score); radar chart (programme skill profile vs. market profile, top 10 skills)
- **For administrators**: Programme-level view only; no student-level data
- **For curriculum designers**: Course-level drill-down from heatmap

## Remaining Uncertainty
Thai academic administrator user research not yet done. Visualisation preferences may vary between Thai HE context and the Chilean/Australian studies cited here. User testing in Phase 4 needed to validate format choices before finalising the report design.
