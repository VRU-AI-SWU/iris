use anyhow::Result;
use std::collections::HashMap;
use sqlx::PgPool;

/// Skill term → weighted score (not yet normalised).
pub type SkillFreq = HashMap<String, f64>;

/// Category weights for analysis scenarios (including internal per-category variants).
pub fn category_weight(category: &str, scenario: &str) -> f64 {
    match scenario {
        "core" => match category {
            "major"   => 1.0,
            "general" => 0.5,
            _         => 0.0,
        },
        "core_electives" => match category {
            "major"    => 1.0,
            "general"  => 0.5,
            "elective" => 0.5,
            _          => 0.0,
        },
        // Internal: isolate a single category for decomposition
        "major_only"    => if category == "major"    { 1.0 } else { 0.0 },
        "general_only"  => if category == "general"  { 1.0 } else { 0.0 },
        "elective_only" => if category == "elective" { 1.0 } else { 0.0 },
        _ => 1.0, // "hypothetical" — equal weight
    }
}

/// Normalise a raw frequency map to a probability distribution (sums to 1).
/// Returns an empty map if total is zero.
pub fn normalise(freq: &SkillFreq) -> SkillFreq {
    let total: f64 = freq.values().sum();
    if total == 0.0 {
        return HashMap::new();
    }
    freq.iter().map(|(k, v)| (k.clone(), v / total)).collect()
}

// ── Programme distribution ────────────────────────────────────────────────────

#[derive(sqlx::FromRow)]
struct CategorySkillRow {
    skill_term: String,
    total_credits: f64,
    category: String,
}

/// Build a weighted skill-frequency map for a programme.
/// Weights skills by (credits × category_weight) summed across courses.
pub async fn programme_skill_freq(
    pool: &PgPool,
    programme_id: i32,
    scenario: &str,
) -> Result<SkillFreq> {
    let rows = sqlx::query_as::<_, CategorySkillRow>(
        r#"
        SELECT cs.skill_term,
               SUM(c.credits) AS total_credits,
               c.category
        FROM course_skills cs
        JOIN courses c ON cs.course_id = c.id
        WHERE c.programme_id = $1
        GROUP BY cs.skill_term, c.category
        "#,
    )
    .bind(programme_id)
    .fetch_all(pool)
    .await?;

    let mut freq: SkillFreq = HashMap::new();
    for row in rows {
        let w = category_weight(&row.category, scenario);
        if w > 0.0 {
            *freq.entry(row.skill_term).or_insert(0.0) += row.total_credits * w;
        }
    }
    Ok(freq)
}

// ── Market distribution ───────────────────────────────────────────────────────

#[derive(sqlx::FromRow)]
struct MarketSkillRow {
    skill_term: String,
    count: i64,
}

/// Build a skill-frequency map from job postings for a given career path.
/// Only counts postings scraped within the last `window_months` months.
pub async fn market_skill_freq(
    pool: &PgPool,
    career_path: &str,
    window_months: i64,
) -> Result<SkillFreq> {
    let rows = sqlx::query_as::<_, MarketSkillRow>(
        r#"
        SELECT js.skill_term, COUNT(*) AS count
        FROM job_skills js
        JOIN job_postings jp ON js.posting_id = jp.id
        WHERE jp.career_path = $1
          AND jp.scraped_at >= NOW() - ($2 || ' months')::INTERVAL
        GROUP BY js.skill_term
        "#,
    )
    .bind(career_path)
    .bind(window_months)
    .fetch_all(pool)
    .await?;

    Ok(rows
        .into_iter()
        .map(|r| (r.skill_term, r.count as f64))
        .collect())
}
