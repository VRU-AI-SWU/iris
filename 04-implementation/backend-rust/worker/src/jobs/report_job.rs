use apalis::prelude::{Data, Error};
use shared::jobs::ReportJob;
use std::sync::Arc;

use crate::{pipeline::report_generator, state::WorkerState};

pub async fn process(
    job: ReportJob,
    state: Data<Arc<WorkerState>>,
) -> Result<(), Error> {
    let pool = &(**state).pool;
    let settings = &(**state).settings;

    tracing::info!(analysis_id = job.analysis_id, "report job started");

    // Load analysis + programme info
    #[derive(sqlx::FromRow)]
    struct AnalysisInfo {
        programme_id: i32,
        career_path: Option<String>,
        compare_programme_id: Option<i32>,
        scenario: String,
    }
    let analysis = sqlx::query_as::<_, AnalysisInfo>(
        "SELECT programme_id, career_path, compare_programme_id, scenario
         FROM gap_analyses WHERE id = $1",
    )
    .bind(job.analysis_id)
    .fetch_one(pool)
    .await
    .map_err(map_db)?;

    #[derive(sqlx::FromRow)]
    struct ProgrammeInfo {
        name: String,
        university: String,
    }
    let prog = sqlx::query_as::<_, ProgrammeInfo>(
        "SELECT name, university FROM programmes WHERE id = $1",
    )
    .bind(analysis.programme_id)
    .fetch_one(pool)
    .await
    .map_err(map_db)?;

    // Determine target label
    let target = if let Some(cp) = &analysis.career_path {
        cp.clone()
    } else if let Some(cmp_id) = analysis.compare_programme_id {
        sqlx::query_scalar::<_, String>("SELECT name FROM programmes WHERE id = $1")
            .bind(cmp_id)
            .fetch_one(pool)
            .await
            .map_err(map_db)?
    } else {
        "Unknown".to_string()
    };

    // Load gap results
    #[derive(sqlx::FromRow)]
    struct GapResultRow {
        kl_divergence: Option<f64>,
        cosine_similarity: Option<f64>,
        ranked_gaps: Option<serde_json::Value>,
        skill_decomposition: Option<serde_json::Value>,
        heatmap_data: Option<serde_json::Value>,
        narrative_summary: Option<String>,
    }
    let result = sqlx::query_as::<_, GapResultRow>(
        "SELECT kl_divergence, cosine_similarity, ranked_gaps,
                skill_decomposition, heatmap_data, narrative_summary
         FROM gap_results WHERE analysis_id = $1",
    )
    .bind(job.analysis_id)
    .fetch_one(pool)
    .await
    .map_err(map_db)?;

    let empty_val = serde_json::Value::Null;
    let ranked_gaps = result.ranked_gaps.as_ref().unwrap_or(&empty_val);
    let decomp = result.skill_decomposition.as_ref().unwrap_or(&empty_val);

    // Tera templates live next to the worker binary in production;
    // in development they're at worker/templates relative to workspace root.
    let templates_dir = std::env::var("TEMPLATES_DIR")
        .unwrap_or_else(|_| "worker/templates".to_string());

    let html_path = report_generator::render_html(
        &settings.reports_dir,
        &templates_dir,
        job.analysis_id,
        &prog.name,
        &prog.university,
        &target,
        &analysis.scenario,
        result.kl_divergence.unwrap_or(0.0),
        result.cosine_similarity.unwrap_or(0.0),
        ranked_gaps,
        decomp,
        result.narrative_summary.as_deref(),
    )
    .await
    .map_err(|e| {
        let io = std::io::Error::new(std::io::ErrorKind::Other, e.to_string());
        Error::Failed(Arc::new(Box::new(io)))
    })?;

    // Store the report path in gap_results
    sqlx::query("UPDATE gap_results SET pdf_path = $2 WHERE analysis_id = $1")
        .bind(job.analysis_id)
        .bind(&html_path)
        .execute(pool)
        .await
        .map_err(map_db)?;

    tracing::info!(analysis_id = job.analysis_id, path = %html_path, "report job complete");
    Ok(())
}

fn map_db(e: sqlx::Error) -> Error {
    Error::Failed(Arc::new(Box::new(e)))
}
