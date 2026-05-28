---
type: paper
authors: Zhen Xu, Xinjin Li, Yingqi Huan, Veronica Minaya, Renzhe Yu
year: 2025
title: "From Course to Skill: Evaluating LLM Performance in Curricular Analytics"
venue: arXiv:2505.02324 (cs.CY)
doi: 10.48550/arXiv.2505.02324
relevance: high
questions: [q-implied-skills, q-skill-taxonomy, q-thai-nlp]
---

## Research Question
How reliably can LLMs extract skills from curriculum documents compared to traditional NLP methods, and which strategies work best for which document types?

## Limitations of Existing Methods
Prior work assumed LLMs perform well for curricular skill extraction without systematic empirical evaluation. No benchmark existed for comparing LLM-based approaches (RAG, zero-shot) against conventional NLP methods on curriculum documents specifically.

## Contribution
Systematic evaluation of four text alignment strategies on a stratified sample of 400 curriculum documents. A collaborative human-LLM evaluation framework for annotation. Evidence-based recommendation of RAG as the preferred strategy.

## Proposed Method
Four strategies compared: RAG, zero-shot LLM prompting, few-shot LLM prompting, and conventional NLP (TF-IDF/keyword matching). Stratified sample of 400 curriculum documents. Evaluation via human-LLM collaborative annotation.

## Key Findings
RAG is the top-performing strategy across all curriculum document types. Zero-shot prompting underperforms conventional NLP in most cases. LLMs handle brief and abstract course descriptions better than longer documents. Performance varies significantly with model selection and prompting approach — no single setting works universally.

## Limitations of This Paper
English curriculum documents only. Human-LLM collaborative evaluation introduces potential annotation bias. RAG performance depends heavily on the quality of the skill knowledge base used for retrieval.

## Concepts
[[curriculum-analytics]] · [[rag-skill-extraction]] · [[llm-skill-extraction]] · [[zero-shot-prompting]] · [[skill-extraction]]

## Questions Addressed
[[q-implied-skills]] · [[q-skill-taxonomy]] · [[q-thai-nlp]]

## Notes for Iris
Critical finding: RAG outperforms zero-shot for curriculum skill extraction. This is a significant challenge for our approach — our current design uses zero-shot LLM extraction from TQF course descriptions. We should consider RAG with a skill knowledge base (even a small one seeded from our emergent vocabulary). The finding that LLMs handle brief, abstract documents well is reassuring given that many TQF course descriptions are short. Zero-shot underperformance is a risk to flag.
