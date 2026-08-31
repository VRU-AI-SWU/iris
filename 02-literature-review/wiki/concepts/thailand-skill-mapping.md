---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](thailand-skill-mapping.th.md)

## Definition
**Thailand Skill Mapping** is the national skill reference database published by the
Office of the Permanent Secretary, Ministry of Higher Education, Science, Research and
Innovation (สป.อว. / OPS MHESI), developed by KMITL under the initiative of
Prof. Dr. Surin Khomfoi. It launched publicly in July 2025.

Structure (snapshot 2026-08-27, API `0.8.1-beta-public`):

| Level | Count | Contents |
|---|---|---|
| Industry | 5 | aviation & logistics, robotics, digital, electric vehicles, smart electronics |
| Career | 371 (138 digital) | Thai description; a demand vector over skills |
| Skill | 4,376 | Thai + English title, Thai definition, `hard-skill` / `soft-skill` / `tools` |

Every skill carries **three proficiency levels** — `ระดับพื้นฐาน`, `ระดับปานกลาง`,
`ระดับสูง` — each with 3–5 explicit written criteria. Every career × skill pair carries
a demand `count`, a `percentage`, and a `growth` rate.

Access: open API at `api.skillmapping.in.th`, no authentication; portals at
[skillmapping.in.th](https://www.skillmapping.in.th/en),
[skill-mapping.ops.go.th](https://skill-mapping.ops.go.th/), and
[skill.kmitl.ac.th](https://skill.kmitl.ac.th/).

## Data characteristics that constrain use
- `percentage` is **prevalence** (share of a career's postings mentioning the skill),
  not a distribution share — values across a career sum to far more than 100
- The demand vector is **truncated at ~100 skills per career**
- Posting counts `N` range 203 – 6,291,725, which is not plausible for Thailand alone —
  corpus provenance is unconfirmed
- 1.4 % of career × skill pairs have `count = 0`; three digital careers are degenerate
- The API is beta; analyses must pin a snapshot

## Papers That Discuss This
*(populated via Obsidian backlinks)*

## Related Concepts
[[skill-entity-linking]] · [[proficiency-levels]] · [[esco-ontology]] · [[tpqi-framework]]

## Relevance to Iris
This is the **foundation the project now stands on**. It supplies, as national reference
data, both halves that the previous design tried to build itself: a controlled skill
vocabulary (replacing the emergent clustering approach) and labour-market demand
(replacing the job-board scrapers).

The platform defines its own purpose as joining a *demand side* to a *supply side* —
what the market wants, and what curricula produce. **Only the demand side is published.**
Iris builds the supply side, which is what makes the project a contribution to national
infrastructure rather than a standalone tool.

It also invalidates the previous answer to [[q-thai-ontology]]: a Thai skill vocabulary
at the granularity Iris needs now exists.
