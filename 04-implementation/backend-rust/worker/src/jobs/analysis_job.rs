use apalis::prelude::{Data, Error};
use shared::jobs::GapAnalysisJob;
use std::sync::Arc;

use crate::{
    pipeline::{
        gap_engine,
        llm_client::LlmClient,
        vocab_builder,
    },
    state::WorkerState,
};

pub async fn process(
    job: GapAnalysisJob,
    state: Data<Arc<WorkerState>>,
) -> Result<(), Error> {
    let pool = &(**state).pool;
    let settings = &(**state).settings;

    tracing::info!(analysis_id = job.analysis_id, "gap analysis job started");

    sqlx::query("UPDATE gap_analyses SET status = 'running' WHERE id = $1")
        .bind(job.analysis_id)
        .execute(pool)
        .await
        .map_err(map_db)?;

    // Load analysis parameters
    #[derive(sqlx::FromRow)]
    struct AnalysisRow {
        programme_id: i32,
        career_path: Option<String>,
        compare_programme_id: Option<i32>,
        scenario: String,
    }

    let analysis = sqlx::query_as::<_, AnalysisRow>(
        "SELECT programme_id, career_path, compare_programme_id, scenario
         FROM gap_analyses WHERE id = $1",
    )
    .bind(job.analysis_id)
    .fetch_one(pool)
    .await
    .map_err(map_db)?;

    // Load programme metadata for narrative
    #[derive(sqlx::FromRow)]
    struct ProgrammeRow {
        name: String,
        university: String,
    }
    let prog = sqlx::query_as::<_, ProgrammeRow>(
        "SELECT name, university FROM programmes WHERE id = $1",
    )
    .bind(analysis.programme_id)
    .fetch_one(pool)
    .await
    .map_err(map_db)?;

    // Build programme skill distribution
    let prog_freq = vocab_builder::programme_skill_freq(
        pool,
        analysis.programme_id,
        &analysis.scenario,
    )
    .await
    .map_err(map_anyhow)?;

    let prog_dist = vocab_builder::normalise(&prog_freq);

    // Build market (or compare-programme) distribution
    let (market_dist, target_name) = if let Some(career_path) = &analysis.career_path {
        let market_freq = vocab_builder::market_skill_freq(
            pool,
            career_path,
            settings.job_posting_window_months as i64,
        )
        .await
        .map_err(map_anyhow)?;
        (vocab_builder::normalise(&market_freq), career_path.clone())
    } else if let Some(cmp_id) = analysis.compare_programme_id {
        let cmp_freq = vocab_builder::programme_skill_freq(pool, cmp_id, &analysis.scenario)
            .await
            .map_err(map_anyhow)?;
        let name: String = sqlx::query_scalar("SELECT name FROM programmes WHERE id = $1")
            .bind(cmp_id)
            .fetch_one(pool)
            .await
            .map_err(map_db)?;
        (vocab_builder::normalise(&cmp_freq), name)
    } else {
        tracing::warn!(analysis_id = job.analysis_id, "analysis has no career_path or compare_programme_id");
        fail_analysis(pool, job.analysis_id, "no target specified").await;
        return Ok(());
    };

    // Compute gap
    let mut gap = gap_engine::compute_gap(&market_dist, &prog_dist);

    // Per-category decomposition for the programme
    let major_freq   = vocab_builder::programme_skill_freq(pool, analysis.programme_id, "major_only")
        .await
        .unwrap_or_default();
    let general_freq = vocab_builder::programme_skill_freq(pool, analysis.programme_id, "general_only")
        .await
        .unwrap_or_default();
    let elective_freq = vocab_builder::programme_skill_freq(pool, analysis.programme_id, "elective_only")
        .await
        .unwrap_or_default();
    gap_engine::add_decomposition(&mut gap, &major_freq, &general_freq, &elective_freq);

    // Narrative via LLM
    let client = LlmClient::new(
        &settings.model_server_url,
        &settings.model_api_key,
        &settings.extraction_model,
        &settings.embedding_model,
    );
    let prompt = gap_engine::build_narrative_prompt(&gap, &prog.name, &target_name);
    let narrative = client
        .generate_narrative(&prompt, 512)
        .await
        .unwrap_or_default();

    // Serialise results to JSON
    let ranked_json = gap_engine::ranked_gaps_to_json(&gap.ranked_gaps);
    let decomp_json = gap_engine::decomposition_to_json(&gap.skill_decomposition);
    let heatmap_json = gap_engine::heatmap_to_json(&gap.heatmap_data);

    // Upsert gap_results row
    sqlx::query(
        r#"
        INSERT INTO gap_results
            (analysis_id, kl_divergence, cosine_similarity,
             ranked_gaps, skill_decomposition, heatmap_data, narrative_summary)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (analysis_id)
        DO UPDATE SET
            kl_divergence      = EXCLUDED.kl_divergence,
            cosine_similarity  = EXCLUDED.cosine_similarity,
            ranked_gaps        = EXCLUDED.ranked_gaps,
            skill_decomposition = EXCLUDED.skill_decomposition,
            heatmap_data       = EXCLUDED.heatmap_data,
            narrative_summary  = EXCLUDED.narrative_summary
        "#,
    )
    .bind(job.analysis_id)
    .bind(gap.kl_divergence)
    .bind(gap.cosine_similarity)
    .bind(&ranked_json)
    .bind(&decomp_json)
    .bind(&heatmap_json)
    .bind(if narrative.is_empty() { None } else { Some(narrative) })
    .execute(pool)
    .await
    .map_err(map_db)?;

    sqlx::query(
        "UPDATE gap_analyses SET status = 'completed', completed_at = NOW() WHERE id = $1",
    )
    .bind(job.analysis_id)
    .execute(pool)
    .await
    .map_err(map_db)?;

    tracing::info!(analysis_id = job.analysis_id, kl = gap.kl_divergence, "gap analysis complete");
    Ok(())
}

// ── Helpers ───────────────────────────────────────────────────────────────────

fn map_db(e: sqlx::Error) -> Error {
    Error::Failed(Arc::new(Box::new(e)))
}

fn map_anyhow(e: anyhow::Error) -> Error {
    let io = std::io::Error::new(std::io::ErrorKind::Other, e.to_string());
    Error::Failed(Arc::new(Box::new(io)))
}

async fn fail_analysis(pool: &sqlx::PgPool, id: i32, reason: &str) {
    let _ = sqlx::query(
        "UPDATE gap_analyses SET status = 'failed' WHERE id = $1",
    )
    .bind(id)
    .execute(pool)
    .await;
    tracing::error!(analysis_id = id, reason, "gap analysis failed");
}
