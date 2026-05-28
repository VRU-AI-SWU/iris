---
type: paper
authors: Hilliger I., Aguirre C., Miranda C., Celis S., Pérez-Sanagustín M.
year: 2022
title: "Lessons learned from designing a curriculum analytics tool for improving student learning and program quality"
venue: Journal of Computing in Higher Education 34 (2022), Springer
doi: 10.1007/s12528-021-09284-2
relevance: high
questions: [q-visualisation]
---

## Research Question
How can a curriculum analytics (CA) tool be designed to support continuous curriculum improvement in higher education, and what lessons can be learned from its deployment?

## Limitations of Existing Methods
Most learning analytics tools focus on individual student behaviour (clickstream, grades), not curriculum-level decision-making for administrators. Existing curriculum reviews are manual, periodic, and not evidence-driven. Administrators lack tools to see competency coverage and gaps across courses simultaneously.

## Contribution
Design, deployment, and evaluation of a web-based curriculum analytics tool across one higher education institution (Chile). Multi-level reporting (student → course → program). User evaluation with administrators (managers) and teaching staff using a validated framework. Lessons learned from two design iterations.

## Proposed Method
- **Tool features**: Drag-and-drop competency-course alignment matrix; automated competency attainment reports (% per course, per program); multi-level aggregated views
- **Visualisation formats used**: Competency attainment percentages; programme-level competency heatmap; course-level comparison table; student progress radar chart
- **Evaluation**: Framework-based usability evaluation; 947 users (one institutional cycle); managers rated 76/100, teaching staff rated 85/100

## Key Findings
- **Administrators (managers) are primary users** for programme-level decision-making; teaching staff use course-level views; students are secondary users
- Multi-level reporting (student / course / program) is essential — administrators want aggregate views, not individual student data
- Administrators valued: *"managing information in high detail at different aggregate levels"* — they want drill-down capability from programme level to course level
- Tool facilitated evidence collection for accreditation: documentary variety increased from 2 to 5 items per course
- Managers rated tool 76/100 (slightly lower than teaching staff 85/100) — administrators are harder to satisfy; their needs are strategic, not pedagogical
- Persistent usability issues: 1/3 of 947 users reported unresolved problems even after redesign — UI simplicity for non-technical users is a major design challenge

## Limitations of This Paper
Single-institution study in Chile; generalisability to Thai university context unconfirmed. COVID-19 disrupted multi-site evaluation. No direct evidence linking tool adoption to improved student learning outcomes. Usability issues were not fully resolved.

## Concepts
[[curriculum-analytics]]

## Questions Addressed
[[q-visualisation]]

## Notes for Iris
**Three UX/UI design principles for Iris gap reports, validated by this study:**
1. **Multi-level output is mandatory**: Programme-level summary + course-level drill-down. Administrators need the programme view; department heads need the course view. Both outputs should be generated automatically.
2. **Administrators are harder to design for than faculty**: Faculty understand the data; administrators want actionable conclusions. Iris gap reports should lead with a clear narrative summary ("Your programme is missing X, Y, Z skills required for the Data Science career path") before showing any charts. The visual detail comes after the headline.
3. **Heatmap for programme × skill matrix**: Combine with ahadi-2022's course × occupation heatmap design — the validated visualisation format for academic stakeholders. Radar charts (used in this tool) are less effective for large skill sets but useful for a 5–10 skill summary view.
