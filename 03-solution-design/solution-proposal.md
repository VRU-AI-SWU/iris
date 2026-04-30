# Solution Proposal — Iris (Skill Gap Analysis)

---

## Problem Recap

Thai academic programmes documented in the TQF format (มคอ.2) are designed with intended learning outcomes but lack a systematic, data-driven mechanism to detect and quantify two types of misalignment: (1) differences in skill profiles between programmes that are rarely made explicit, and (2) drift between what programmes teach and what the job market currently demands for a given career path. Academic administrators, curriculum designers, and students make decisions without access to objective, reproducible evidence of these gaps, resulting in graduates who are underprepared for specific careers and institutions that waste resources on outdated content.

---

## Proposed Solution

Iris is an automated skill gap analysis system that extracts skill profiles from TQF course description text using a multilingual LLM, builds comparable skill distributions across programmes, and quantifies gaps between those distributions and against job market demand aggregated from Thai job posting platforms. Outputs are multi-level curriculum analytics reports — a programme-level heatmap with narrative summary for academic administrators, and a course-level skill breakdown for curriculum designers. The system also supports programme-to-programme comparison and scenario-based "what-if" curriculum planning.

---

## How It Addresses the Gaps

| Gap / Pain Point | How Iris Addresses It |
|---|---|
| No systematic method to compare skill profiles across Thai programmes | Builds comparable skill distributions from TQF documents using a unified extraction pipeline; supports head-to-head programme comparison with set-based skill decomposition |
| Curriculum drift from job market not detectable until graduates are already underprepared | Aggregates 1,000–2,000 job postings per career path from 4 confirmed Thai platforms within a 12-month window; KL divergence quantifies the current gap |
| Gap analysis outputs are not interpretable by non-technical stakeholders | Heatmap (courses × skills) validated in literature as the most interpretable format for academic administrators; narrative summary accompanies all reports |
| No Thai skill ontology exists for grounding extraction | Data-driven emergent vocabulary — skills are extracted bottom-up from actual document text, not forced into a pre-defined taxonomy |
| Existing tools are not designed for Thai TQF context | Parser built specifically for TQF (มคอ.2) structure; extraction handles Thai text natively via multilingual LLM |

---

## Use Cases

### Use Case 1: Programme-to-Market Gap Report
- **Actor:** Academic administrator or curriculum designer
- **Goal:** Understand how their CS programme's skill profile compares to market demand for a specific career path (e.g., Data Engineer)
- **Preconditions:** TQF document for the programme has been uploaded; job posting dataset for the target career path is available
- **Main flow:**
  1. User selects a programme from the programme library
  2. User selects a target career path from the 20-role Thai digital taxonomy
  3. System computes skill distribution for the programme (credit-weighted, major courses prioritised)
  4. System computes market demand distribution for the career path from job postings
  5. System calculates KL divergence (market‖programme) and RCA-weighted skill gap ranking
  6. System generates: programme-level heatmap, ranked gap table, narrative summary
- **Outcome:** Administrator receives a prioritised list of skill gaps with course-level traceability, ready for curriculum review

### Use Case 2: Programme-to-Programme Comparison
- **Actor:** Academic administrator or accreditation reviewer
- **Goal:** Understand how two programmes differ in their skill profiles
- **Preconditions:** TQF documents for both programmes are in the system
- **Main flow:**
  1. User selects two programmes to compare
  2. System builds shared emergent skill vocabulary from the union of both programmes
  3. System decomposes skills into: common skills (shared baseline), A-unique skills, B-unique skills
  4. System generates side-by-side comparison view with skill overlap and divergence summary
- **Outcome:** Clear quantified picture of where two programmes converge and diverge, useful for differentiation or merger decisions

### Use Case 3: Curriculum Scenario Planning
- **Actor:** Curriculum designer
- **Goal:** Explore how adding or removing courses would affect the programme's skill profile and gap scores
- **Preconditions:** Base programme is already analysed; user has a set of candidate courses to add
- **Main flow:**
  1. User opens the scenario builder for a programme
  2. User selects a scenario: Core only / Core + selected electives / Hypothetical (add/remove any courses)
  3. System recomputes skill distribution and gap scores under the new scenario
  4. System shows side-by-side comparison: current vs. proposed scenario
- **Outcome:** Curriculum designer can see the skill impact of proposed changes before committing to a redesign

### Use Case 4: Student Career Path Alignment
- **Actor:** Student or career advisor
- **Goal:** Understand how well the student's enrolled programme aligns with a target career path, and identify personal skill gaps to address
- **Preconditions:** Programme is in the system; user selects a career path
- **Main flow:**
  1. User selects their programme and a target career path
  2. System displays programme coverage vs. career path requirements
  3. System highlights skills not covered by the programme that the career path demands
- **Outcome:** Student understands which skills to develop independently; advisor has data to guide planning

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                            │
│  Web App (React)  ←→  REST API (FastAPI)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                                                              │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │  Gap Analysis   │    │     Report Generator          │   │
│  │  Engine         │    │  (heatmap, narrative, PDF)    │   │
│  │  - KL divergence│    └──────────────────────────────┘   │
│  │  - RCA weighting│                                        │
│  │  - Set decomp.  │    ┌──────────────────────────────┐   │
│  └────────┬────────┘    │   Scenario Engine             │   │
│           │             │   (Core / +Electives / Hypo.) │   │
│  ┌────────▼────────┐    └──────────────────────────────┘   │
│  │  Skill Vocab    │                                        │
│  │  Builder        │                                        │
│  │  - Clustering   │                                        │
│  │  - ESCO mapping │                                        │
│  └────────┬────────┘                                        │
└───────────┼─────────────────────────────────────────────────┘
            │
┌───────────┼─────────────────────────────────────────────────┐
│           │          INGESTION LAYER                         │
│  ┌────────▼──────────┐    ┌─────────────────────────────┐  │
│  │  TQF Pipeline     │    │  Job Posting Pipeline        │  │
│  │  - PDF parse      │    │  - Scrapy (4 platforms)      │  │
│  │  - PyThaiNLP prep │    │  - Unified schema adapter    │  │
│  │  - LLM extraction │    │  - LLM skill extraction      │  │
│  │  - Embedding      │    │  - Embedding                 │  │
│  └───────────────────┘    └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
            │
┌───────────┼─────────────────────────────────────────────────┐
│           │          INFRASTRUCTURE LAYER                    │
│  ┌────────▼───────────────────────────────────────────┐     │
│  │  Model Server (Ollama container — production)       │     │
│  │  Model Server (LM Studio — dev)                    │     │
│  │  - gemma-4-31b-it (extraction)                     │     │
│  │  - text-embedding-embeddinggemma-300m (embedding)  │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  PostgreSQL — programmes, courses, skills, postings │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Key components:**

| Component | Responsibility | Technology |
|---|---|---|
| TQF Parser | Extracts course list, descriptions, credit hours, and category (major/general/elective) from TQF PDF | Python, pdftotext / pdfplumber |
| Thai Preprocessor | Tokenisation, segmentation, stop word removal on Thai text | PyThaiNLP |
| Skill Extractor | Extracts skill terms from course descriptions and job posting text | gemma-4-31b-it via OpenAI-compatible API |
| Skill Embedder | Generates vector representations of extracted skill terms | text-embedding-embeddinggemma-300m |
| Skill Vocabulary Builder | Clusters semantically similar skills; builds shared vocabulary across programmes | scikit-learn (HDBSCAN or k-means), cosine similarity |
| Job Posting Scraper | Scrapes job postings from 4 Thai platforms with unified schema | Scrapy, BeautifulSoup |
| Gap Analysis Engine | Computes KL divergence, RCA-weighted ranking, and set-based decomposition | Python, scipy, numpy |
| Scenario Engine | Recomputes skill distributions under user-defined course inclusion/exclusion scenarios | Python |
| Report Generator | Produces heatmap, ranked gap tables, and narrative summary | matplotlib / seaborn (heatmap), Jinja2 (narrative), WeasyPrint (PDF) |
| REST API | Exposes all analysis functions to the frontend | FastAPI |
| Web Application | Interactive dashboard for all user personas | React |
| Model Server (dev) | Serves LLM and embedding models via OpenAI-compatible API | LM Studio on gpu-linux-server host, port 1234 |
| Model Server (prod) | Serves LLM and embedding models via OpenAI-compatible API | Ollama Docker container on CSML, models volume-mounted from host |
| Database | Stores programmes, courses, extracted skills, job postings, computed distributions | PostgreSQL |

---

## AI / ML Components

### 1. Skill Extraction (LLM)
- **Model:** `gemma-4-31b-it` (multilingual, handles Thai natively)
- **Approach:** Zero-shot prompt — given a course description, extract a list of technical skills as a JSON array
- **Input:** Course description text (Thai or bilingual), job posting requirements text
- **Output:** List of skill terms per document
- **Constraint:** v1 uses zero-shot; RAG-enhanced extraction earmarked for v2

### 2. Skill Embedding
- **Model:** `text-embedding-embeddinggemma-300m`
- **Purpose:** Generate dense vectors for extracted skill terms to enable semantic clustering and similarity matching
- **Output:** 300-dimensional embedding per skill term

### 3. Skill Vocabulary Construction
- **Method:** Cluster skill embeddings using HDBSCAN (density-based, no fixed cluster count) or agglomerative clustering; representative term per cluster becomes the canonical skill label
- **Output:** Shared skill vocabulary — a flat list of canonical skill labels with cluster membership mapping
- **Optional:** Post-hoc ESCO taxonomy alignment for cross-context comparability

### 4. Skill Distribution Construction
- **Programme distribution:** Frequency of each canonical skill across all courses, weighted by credit hours (major-specific courses weighted higher than general education; free electives excluded in Core scenario)
- **Market distribution:** Frequency of each canonical skill across job postings for a target career path within the 12-month collection window

### 5. Gap Quantification
- **Primary metric:** KL divergence in the market‖programme direction — D_KL(market ‖ programme) — quantifies what the market demands that the programme does not cover
- **Skill ranking:** RCA (Revealed Comparative Advantage) weights each skill by its career-path specificity; penalises common cross-path skills, rewards discriminating skills
- **Programme-to-programme:** Set-based decomposition into common, A-unique, and B-unique skill sets; cosine similarity for aggregate score

---

## Data Requirements

| Data Source | Type | Volume (est.) | Availability | Owner |
|---|---|---|---|---|
| TQF PDFs (มคอ.2) | Structured PDF documents | 2–10 documents per analysis run | Publicly available from Thai university websites | Academic institutions |
| Job postings — Jobthai.com | Web-scraped structured text | 1,000–2,000 per career path per 12-month window | Publicly accessible; confirmed in academic research | Jobthai.com |
| Job postings — Jobsdb Thailand | Web-scraped structured text | Supplementary to Jobthai target | Publicly accessible; third-party scrapers available | Jobsdb Thailand |
| Job postings — JOBBKK.com | Web-scraped structured text | Supplementary | Publicly accessible; confirmed academic research | JOBBKK |
| Job postings — JOBTOPGUN.com | Web-scraped structured text | Supplementary; tech/professional focus | Publicly accessible; confirmed academic research | JOBTOPGUN |

**Data ethics notes:**
- Collect job posting metadata only (title, description, requirements, company, date) — no applicant PII
- Thai PDPA 2019 applies; company names and job requirements are not personal data
- Collection date range must be documented for reproducibility (academic publication requirement)
- Static snapshot for v1; no live continuous scraping

---

## Infrastructure Design

### Development Environment
```
gpu-linux-server (RTX 3090, 32GB RAM)
├── LM Studio (host, port 1234)
│   ├── gemma-4-31b-it
│   └── text-embedding-embeddinggemma-300m
├── PostgreSQL (host or Docker)
└── Iris services (run locally, call LM Studio at localhost:1234)
```

### Production Environment (CSML)
```
CSML Server (NVIDIA A30 24GB, 512GB RAM)
├── /home/comsci/models/          ← models on host filesystem
│   ├── gemma-4-31b-it
│   └── text-embedding-embeddinggemma-300m
└── docker-compose (production stack)
    ├── ollama (model server container)
    │   └── volume: /home/comsci/models → /root/.ollama/models
    ├── iris-api (FastAPI backend)
    ├── iris-web (React frontend, nginx)
    ├── iris-worker (pipeline workers — scraping, extraction, analysis)
    └── postgres (database)
```

**Pre-deployment requirement:** Disable MIG on CSML A30 (`sudo nvidia-smi --mig 0`) to allow full GPU allocation to the Ollama container.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM extraction quality on formal Thai TQF text is unvalidated | Medium | High | Manual evaluation on sample of 50 course descriptions before full pipeline run; adjust prompt if recall is low |
| Job posting platform ToS changes or scraping blocks | Medium | Medium | Scrape once for v1 dataset; document collection date; add rate limiting and respectful crawl delays |
| CSML is a shared department resource — GPU may not always be available | Medium | Medium | Queue-based pipeline; extract and store results in DB so re-inference is not needed per query; design for async processing |
| MIG configuration on CSML A30 causing reduced GPU performance | Low (fixable) | High | Disable MIG before deployment (`nvidia-smi --mig 0`); verify with `nvidia-smi` post-disable |
| Emergent skill vocabulary instability across runs | Low | Medium | Fix vocabulary snapshot after initial construction; only update vocabulary when new programmes are added via explicit re-clustering step |
| Thai PDPA compliance for job posting data | Low | High | Collect only non-personal job metadata; document data handling in methods section of paper |

---

## Alternatives Considered

| Alternative | Reason Not Selected |
|---|---|
| WangchanBERTa for Thai skill extraction | Fails to discriminate closely related Thai terms (97.21% cosine similarity between Physician/Dentist — lertmethaphat-2025); would collapse skill distinctions essential to the analysis |
| Fixed skill taxonomy (O*NET, ESCO, SFIA) | No Thai-language version exists; imposing an English taxonomy on Thai TQF text would introduce translation noise and miss domain-specific terms; emergent vocabulary is more honest |
| Symmetric gap metric | Directional KL divergence is more actionable — administrators need to know what graduates lack (market‖programme direction), not what they have in excess |
| Live job posting scraping | Increases v1 complexity; temporal stability of static snapshot is sufficient for academic publication and initial institutional use; live scraping earmarked for v2 |
| RAG-based curriculum extraction | Validated as superior to zero-shot (xu-2025) but requires a retrieval corpus not yet available; earmarked for v2 |
| Single-container deployment | Tightly couples model server, application, and database; harder to update and scale; multi-container docker-compose is the correct architecture for the CSML environment |

---

## Open Technical Questions

- What credit-hour weighting function best reflects a course's contribution to the programme skill profile? (empirical — Phase 4)
- What is the optimal HDBSCAN parameter set (min_cluster_size, min_samples) for the Thai skill term embedding space? (empirical — Phase 4)
- How reliable is gemma-4-31b-it zero-shot extraction on sparse TQF course descriptions (1–3 sentences)? (requires manual evaluation on sample — early Phase 4)
- What prompt template produces the most accurate skill extraction from bilingual (Thai+English) TQF descriptions? (empirical — Phase 4)
- Will Ollama serve `text-embedding-embeddinggemma-300m` (a custom Unsloth-quantized model) or does a custom inference endpoint need to be built? (technical investigation — early Phase 4)
- Does disabling MIG on CSML A30 require a reboot? (operational — pre-deployment check)

---

_Phase complete when: Architecture is agreed, use cases are validated with stakeholders, product design is complete, and the team can begin detailed design and implementation._
