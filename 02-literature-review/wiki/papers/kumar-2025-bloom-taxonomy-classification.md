---
type: paper
authors: [Kumar R., Gulwani D., Singh S.]
year: 2025
title: "Automated Analysis of Learning Outcomes and Exam Questions Based on Bloom's Taxonomy"
venue: arXiv (cs.CL) 2511.10903
doi: 10.48550/arXiv.2511.10903
relevance: high
questions: [q-level-inference, q-credit-weighting]
---

## Research Question
Which model family best classifies learning outcomes and exam questions into Bloom's
Taxonomy cognitive levels, given that labelled data in this domain is scarce?

## Limitations of Existing Methods
Deep architectures overfit badly on the small datasets typical of educational-outcome
research. Prior work reported single-model results without a controlled comparison across
model families on the same data.

## Contribution
A like-for-like comparison spanning classical ML, RNNs, transformers, and frontier LLMs on
one Bloom's-classification dataset, showing that a simple augmented model beats every more
complex option.

## Proposed Method
- **Dataset:** 600 labelled sentences across the six Bloom's cognitive levels — Knowledge,
  Comprehension, Application, Analysis, Synthesis, Evaluation
- **Models:** Naive Bayes, Logistic Regression, SVM · LSTM, BiLSTM, GRU, BiGRU · BERT,
  RoBERTa · LLMs from OpenAI, Gemini, Ollama, Anthropic
- **Preprocessing:** synonym replacement, word embeddings, data augmentation

## Key Findings

| Approach | Result |
|---|---|
| **SVM + augmentation** | **94%** accuracy, recall and F1, minimal overfitting |
| RNN family (LSTM/BiLSTM/GRU/BiGRU) | severe overfitting |
| BERT | severe overfitting |
| RoBERTa | overfitting initially overcome, then degraded during training |
| **LLMs, zero-shot** | **0.72–0.73** accuracy (OpenAI, Gemini) |

The headline is the ordering: a classical model with augmentation beat both fine-tuned
transformers and zero-shot frontier LLMs by more than 20 points.

## Limitations of This Paper
600 sentences is very small, and the 94% figure is obtained on augmented data, so
generalisation to unseen institutional phrasing is unverified. English only. No
inter-annotator agreement reported for the gold Bloom labels, which matters because Bloom
level is a genuinely contested judgement. Six Bloom levels is a different granularity from
the three levels of the Thai standard.

## Concepts
[[proficiency-levels]] · [[curriculum-analytics]] · [[skill-entity-linking]]

## Questions Addressed
[[q-level-inference]] · [[q-credit-weighting]]

## Notes for the Project
The most useful negative result in the new corpus. Iris's level inference could have been
implemented as "ask the LLM what level this course teaches this skill at"; this paper
measures that approach at **0.72–0.73 accuracy zero-shot on a six-way problem**, well
behind a classical classifier on the same data.

That is a direct argument for the design [[q-level-inference]] specifies: **derive level
from the document's own declared signals** — CLO verbs, the ● / ○ curriculum mapping table,
curriculum position — rather than from an LLM's holistic judgement of a course
description. Bloom's cognitive verbs are exactly the feature an SVM exploits here, and
Thai TQF CLOs are written with the same verb conventions (`อธิบาย` explain → lower;
`ออกแบบ` design → higher).

Two practical consequences:

1. **Include a non-LLM baseline in the Sprint 4 ablation.** A verb-feature classifier over
   CLO text is cheap, and this paper suggests it may win. Iris should not discover that
   after building an LLM-only path.
2. **The three levels of the Thai standard are coarser than Bloom's six**, which should
   make the problem easier — but the standard's criteria are written as *observable
   capabilities*, not cognitive verbs, so the mapping from CLO verb to standard level is
   itself an empirical question for the gate.

The absent inter-annotator agreement is a warning worth heeding: Iris's own protocol must
report it, because if two experts cannot agree on a level, no model result on that data
means anything.
