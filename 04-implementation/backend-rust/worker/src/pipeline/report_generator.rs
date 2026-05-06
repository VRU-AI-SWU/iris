use anyhow::{Context, Result};
use chrono::Utc;
use serde_json::Value;
use std::path::Path;
use tera::{Context as TeraCtx, Tera};

/// Render an HTML gap report and write it to `reports_dir/{analysis_id}.html`.
/// Returns the absolute file path.
pub async fn render_html(
    reports_dir: &str,
    templates_dir: &str,
    analysis_id: i32,
    programme_name: &str,
    university: &str,
    target: &str,
    scenario: &str,
    kl_divergence: f64,
    cosine_similarity: f64,
    ranked_gaps: &Value,
    skill_decomposition: &Value,
    narrative: Option<&str>,
) -> Result<String> {
    let glob = format!("{templates_dir}/report.html");
    let tera = Tera::new(&glob).context("failed to load Tera templates")?;

    let mut ctx = TeraCtx::new();
    ctx.insert("programme_name", programme_name);
    ctx.insert("university", university);
    ctx.insert("target", target);
    ctx.insert("scenario", scenario);
    ctx.insert("kl_divergence", &format!("{kl_divergence:.4}"));
    ctx.insert("cosine_pct", &format!("{:.1}", cosine_similarity * 100.0));
    ctx.insert("narrative", &narrative.unwrap_or(""));
    ctx.insert("generated_at", &Utc::now().format("%Y-%m-%d %H:%M UTC").to_string());

    // ranked_gaps is a JSON array of RankedSkill objects
    let gaps = ranked_gaps.as_array().cloned().unwrap_or_default();
    ctx.insert("ranked_gaps", &gaps);

    // skill_decomposition: {major: [...], general: [...], elective: [...]}
    let empty_arr = Value::Array(vec![]);
    let major_skills = skill_decomposition.get("major").unwrap_or(&empty_arr);
    let general_skills = skill_decomposition.get("general").unwrap_or(&empty_arr);
    let elective_skills = skill_decomposition.get("elective").unwrap_or(&empty_arr);
    ctx.insert("major_skills", major_skills);
    ctx.insert("general_skills", general_skills);
    ctx.insert("elective_skills", elective_skills);

    let html = tera
        .render("report.html", &ctx)
        .context("Tera render failed")?;

    // Write to reports_dir
    let out_path = Path::new(reports_dir).join(format!("{analysis_id}.html"));
    tokio::fs::create_dir_all(reports_dir)
        .await
        .context("create reports_dir")?;
    tokio::fs::write(&out_path, html)
        .await
        .context("write report HTML")?;

    tracing::info!(analysis_id, path = %out_path.display(), "HTML report written");
    Ok(out_path.to_string_lossy().into_owned())
}
