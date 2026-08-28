---
type: concept
---

## Definition
**Thai BERT** refers to transformer encoders pretrained on Thai text.
[[wangchanberta]] ([[lowphansirikul-2021-wangchanberta]]) is the reference model: a
[[roberta-architecture]] encoder trained on a large Thai corpus, outperforming multilingual
baselines (mBERT, XLM-R) on standard Thai benchmarks.

Its value is representing Thai without the dilution multilingual models suffer, where Thai
competes for capacity with a hundred other languages.

Its documented weakness is the one that matters for skill work.
[[lertmethaphat-2025-thai-job-market-nlp]] found WangchanBERTa unable to discriminate
closely related Thai occupational terms — **97.21% cosine similarity between Physician and
Dentist** — collapsing exactly the fine distinctions an occupational application depends
on. Universal Sentence Encoder with XGBoost reached ~90% on the same task.

## Papers That Discuss This
- [[lowphansirikul-2021-wangchanberta]] — the model; SOTA on Thai benchmarks over
  mBERT/XLM-R
- [[lertmethaphat-2025-thai-job-market-nlp]] — ⚠️ the disqualifying finding: 97.21%
  similarity between Physician and Dentist; USE+XGBoost (~90%) preferred
- [[nonesung-2026-typhoon-ocr]] · [[nonesung-2025-thaiocrbench]] — the current generation
  of Thai models is vision-language, not encoder-only

## Related Concepts
[[wangchanberta]] · [[thai-nlp]] · [[roberta-architecture]] · [[sentence-embedding]] ·
[[thai-tokenization]]

## Relevance to Iris
**Excluded from the linking pipeline, on evidence.**

Iris's candidate retrieval must separate `การสร้างแบบจำลองข้อมูลเชิงสัมพันธ์` (Relational
Data Modeling) from `การสร้างแบบจำลองข้อมูลเชิงตรรกะ` (Logical Data Modeling) — Thai
phrases differing in one word, both real entries in the national vocabulary. That is the
Physician/Dentist problem exactly, and the model that fails it cannot do the retrieval
step.

Iris instead needs a **multilingual embedding model** for two reasons beyond
discrimination: the skill vocabulary is bilingual, and course descriptions code-switch
constantly, so the embedding space must hold Thai and English terms together. A Thai-only
encoder cannot represent `React.js` and `การพัฒนาเว็บ` in one space.

Model selection is deferred to the Sprint 4 ablation and decided on measured retrieval
recall, not on benchmark reputation. The lesson from this concept is why: WangchanBERTa is
genuinely state of the art on Thai benchmarks and genuinely unusable here. See
[[q-thai-nlp]].
