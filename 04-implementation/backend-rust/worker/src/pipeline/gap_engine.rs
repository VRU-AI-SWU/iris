use serde::{Deserialize, Serialize};
use std::collections::HashSet;

use super::vocab_builder::SkillFreq;

const EPSILON: f64 = 1e-9;

// ── Output types ──────────────────────────────────────────────────────────────

#[derive(Debug, Serialize, Deserialize)]
pub struct RankedSkill {
    pub skill: String,
    pub market_weight: f64,
    pub programme_weight: f64,
    /// Positive = market needs this more than programme teaches (deficit).
    pub gap_score: f64,
    /// Revealed Comparative Advantage < 1 means programme under-covers this skill.
    pub rca: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct HeatmapEntry {
    pub skill: String,
    pub market_score: f64,
    pub programme_score: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CategoryBreakdown {
    pub skill: String,
    pub weight: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SkillDecomposition {
    pub major: Vec<CategoryBreakdown>,
    pub general: Vec<CategoryBreakdown>,
    pub elective: Vec<CategoryBreakdown>,
}

#[derive(Debug)]
pub struct GapEngineOutput {
    /// KL(market ‖ programme) — divergence of market from programme.
    pub kl_divergence: f64,
    pub cosine_similarity: f64,
    /// Top-50 skills sorted by gap_score descending.
    pub ranked_gaps: Vec<RankedSkill>,
    /// Per-category skill weights from the programme distribution.
    pub skill_decomposition: SkillDecomposition,
    /// Top-30 skills for the comparison heatmap.
    pub heatmap_data: Vec<HeatmapEntry>,
}

// ── Core computation ──────────────────────────────────────────────────────────

/// Compute all gap metrics given normalised probability distributions.
/// `market_p` = Q, `programme_p` = P.
/// Both maps must already be normalised (sum ≈ 1).
pub fn compute_gap(market_p: &SkillFreq, programme_p: &SkillFreq) -> GapEngineOutput {
    let vocab: HashSet<&String> = market_p.keys().chain(programme_p.keys()).collect();

    // KL(Q || P) = Σ Q(x) * log(Q(x) / P(x))
    let mut kl = 0.0_f64;
    for skill in &vocab {
        let q = *market_p.get(*skill).unwrap_or(&0.0);
        let p = *programme_p.get(*skill).unwrap_or(&0.0) + EPSILON;
        if q > 0.0 {
            kl += q * (q / p).ln();
        }
    }

    // Cosine similarity
    let dot: f64 = vocab
        .iter()
        .map(|s| market_p.get(*s).unwrap_or(&0.0) * programme_p.get(*s).unwrap_or(&0.0))
        .sum();
    let mag_m: f64 = market_p.values().map(|v| v * v).sum::<f64>().sqrt();
    let mag_p: f64 = programme_p.values().map(|v| v * v).sum::<f64>().sqrt();
    let cosine = if mag_m > 0.0 && mag_p > 0.0 { dot / (mag_m * mag_p) } else { 0.0 };

    // Ranked gaps
    let mut ranked: Vec<RankedSkill> = vocab
        .iter()
        .map(|skill| {
            let q = *market_p.get(*skill).unwrap_or(&0.0);
            let p = *programme_p.get(*skill).unwrap_or(&0.0);
            let rca = if q > 0.0 { (p + EPSILON) / (q + EPSILON) } else { 1.0 };
            RankedSkill {
                skill: (*skill).clone(),
                market_weight: q,
                programme_weight: p,
                gap_score: q - p,
                rca,
            }
        })
        .collect();
    ranked.sort_by(|a, b| b.gap_score.partial_cmp(&a.gap_score).unwrap());
    ranked.truncate(50);

    // Heatmap (top-30 by market weight)
    let mut heatmap_skills: Vec<&String> = market_p.keys().collect();
    heatmap_skills.sort_by(|a, b| {
        market_p[*b].partial_cmp(&market_p[*a]).unwrap()
    });
    let heatmap = heatmap_skills
        .into_iter()
        .take(30)
        .map(|s| HeatmapEntry {
            skill: s.clone(),
            market_score: *market_p.get(s).unwrap_or(&0.0),
            programme_score: *programme_p.get(s).unwrap_or(&0.0),
        })
        .collect();

    GapEngineOutput {
        kl_divergence: kl,
        cosine_similarity: cosine,
        ranked_gaps: ranked,
        skill_decomposition: SkillDecomposition {
            major: vec![],
            general: vec![],
            elective: vec![],
        },
        heatmap_data: heatmap,
    }
}

/// Populate the skill_decomposition field from per-category raw (un-normalised) freq maps.
pub fn add_decomposition(
    output: &mut GapEngineOutput,
    major_freq: &SkillFreq,
    general_freq: &SkillFreq,
    elective_freq: &SkillFreq,
) {
    output.skill_decomposition.major   = top_skills(major_freq, 20);
    output.skill_decomposition.general = top_skills(general_freq, 20);
    output.skill_decomposition.elective = top_skills(elective_freq, 20);
}

fn top_skills(freq: &SkillFreq, n: usize) -> Vec<CategoryBreakdown> {
    let total: f64 = freq.values().sum::<f64>().max(EPSILON);
    let mut pairs: Vec<(&String, f64)> = freq.iter().map(|(k, v)| (k, v / total)).collect();
    pairs.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    pairs
        .into_iter()
        .take(n)
        .map(|(skill, weight)| CategoryBreakdown { skill: skill.clone(), weight })
        .collect()
}

// ── Narrative prompt builder ──────────────────────────────────────────────────

pub fn build_narrative_prompt(
    output: &GapEngineOutput,
    programme_name: &str,
    target: &str, // career path name or compare programme name
) -> String {
    let top5: Vec<&str> = output
        .ranked_gaps
        .iter()
        .take(5)
        .map(|r| r.skill.as_str())
        .collect();

    format!(
        "You are an expert in curriculum design and labour market analysis for Thai universities.\n\
         Analyse the skill gap between the programme \"{programme_name}\" and the target \"{target}\".\n\n\
         Metrics:\n\
         - KL divergence (market‖programme): {kl:.4}  (higher = larger gap)\n\
         - Cosine similarity: {cos:.4}  (lower = less aligned)\n\
         - Top 5 deficit skills (market needs these more than programme teaches):\n  {top5}\n\n\
         Write a concise 3-paragraph summary (150–200 words) that:\n\
         1. States the overall gap severity\n\
         2. Highlights the most critical missing skills and why they matter\n\
         3. Gives one concrete, actionable curriculum improvement recommendation\n\n\
         Summary:",
        programme_name = programme_name,
        target = target,
        kl = output.kl_divergence,
        cos = output.cosine_similarity,
        top5 = top5.join(", "),
    )
}

// ── Serialisation helpers ─────────────────────────────────────────────────────

pub fn ranked_gaps_to_json(gaps: &[RankedSkill]) -> serde_json::Value {
    serde_json::to_value(gaps).unwrap_or(serde_json::Value::Array(vec![]))
}

pub fn decomposition_to_json(decomp: &SkillDecomposition) -> serde_json::Value {
    serde_json::to_value(decomp).unwrap_or(serde_json::Value::Null)
}

pub fn heatmap_to_json(heatmap: &[HeatmapEntry]) -> serde_json::Value {
    serde_json::to_value(heatmap).unwrap_or(serde_json::Value::Array(vec![]))
}
