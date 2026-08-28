---
type: concept
---

## Definition
A **proficiency level** grades how deeply a skill is held, rather than recording it as
present or absent. Competency frameworks that define levels usually attach observable
criteria to each, so the level can be assessed rather than asserted.

The Thai national standard ([[thailand-skill-mapping]]) defines three for every one of
its 4,376 skills — `ระดับพื้นฐาน` / `ระดับปานกลาง` / `ระดับสูง` — each with 3–5 written
criteria. For `ภาษาไพธอน` (Python):

| Level | First criterion |
|---|---|
| พื้นฐาน | เข้าใจไวยากรณ์พื้นฐานของ Python และประเภทข้อมูล |
| ปานกลาง | สามารถใช้งานฟังก์ชัน โมดูล และการจัดการข้อผิดพลาดได้อย่างมีประสิทธิภาพ |
| สูง | สามารถออกแบบและพัฒนาแอปพลิเคชันและระบบ Python ที่ซับซ้อนได้ |

## The TQF side has its own depth signals
Thai มคอ.2 documents declare depth under regulation, independent of any inference:

1. **Course learning outcomes (CLOs)** — written per course in newer OBE-format documents
2. **แผนที่แสดงการกระจายความรับผิดชอบ (Curriculum Mapping)** — marks each course ×
   learning-outcome pair as ● *ความรับผิดชอบหลัก* or ○ *ความรับผิดชอบรอง*
3. **Curriculum position** — year of study encoded in the course code, and prerequisite depth

This gives three independent evidence sources for level inference, so the level need not
be guessed from a course description alone.

## Papers That Discuss This
- [[kumar-2025-bloom-taxonomy-classification]] — ⚠️ **zero-shot LLMs reach only 0.72–0.73**
  on six-way Bloom classification, while SVM with augmentation reaches 94%; a direct
  argument against asking an LLM to judge level holistically
- [[zaki-2023-clo-plo-mapping-automation]] — automating the CLO→PLO matrix reaches
  **83.1% / 88.1%** precision against domain experts; a caution that the ● ○ matrix Iris
  reads is itself hand-authored and noisy
- [[le-2026-competency-tagging-evidence]] — competency tagging with required evidence spans
  and graph constraints; micro-F1 0.57 over 22 competencies
- [[saroglou-2025-esco-eqf-linking]] — links qualification *levels* (EQF) as well as
  entities; precedent for level as a linking target
- [[sabet-2024-course-skill-atlas]] · [[ahadi-2022-skills-taught-vs-sought]] — both treat
  skills as **binary presence**, confirming the gap Iris addresses

## Related Concepts
[[thailand-skill-mapping]] · [[skill-entity-linking]] · [[tpqi-framework]] · [[curriculum-analytics]]

## Relevance to Iris
Level-awareness is the project's **novel contribution**. The curriculum-analytics
literature reviewed in Phase 2 — [[sabet-2024-course-skill-atlas]],
[[ahadi-2022-skills-taught-vs-sought]] — treats skills as binary presence in a
course×skill matrix. None grade depth.

The combination that makes it possible is specific to this context: a national standard
that publishes graded criteria, and a national curriculum format that requires
programmes to declare outcome responsibility. Iris joins the two, changing the question
from *"does this programme teach X?"* to *"to what level, and is that the level the
career requires?"*

Open question: [[q-level-inference]].
