use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use chrono::Utc;
use serde::{Deserialize, Serialize};

use crate::{
    error::{AppError, Result},
    queue,
    state::AppState,
};
use shared::{jobs::GapAnalysisJob, models::analysis::GapAnalysis};

// ── Request / response types ───────────────────────────────────────────────────

#[derive(Deserialize)]
pub struct AnalysisRequest {
    pub programme_id: i32,
    pub career_path: Option<String>,
    pub compare_programme_id: Option<i32>,
    #[serde(default = "default_scenario")]
    pub scenario: String,
}

fn default_scenario() -> String {
    "core".into()
}

#[derive(Serialize)]
pub struct AnalysisOut {
    pub id: i32,
    pub programme_id: i32,
    pub career_path: Option<String>,
    pub compare_programme_id: Option<i32>,
    pub scenario: String,
    pub status: String,
    pub celery_task_id: Option<String>,
    pub created_at: chrono::NaiveDateTime,
    pub completed_at: Option<chrono::NaiveDateTime>,
}

impl From<GapAnalysis> for AnalysisOut {
    fn from(a: GapAnalysis) -> Self {
        Self {
            id: a.id,
            programme_id: a.programme_id,
            career_path: a.career_path,
            compare_programme_id: a.compare_programme_id,
            scenario: a.scenario,
            status: a.status,
            celery_task_id: a.celery_task_id,
            created_at: a.created_at,
            completed_at: a.completed_at,
        }
    }
}

#[derive(Serialize)]
pub struct AnalysisStatus {
    pub analysis_id: i32,
    pub status: String,
    pub celery_task_id: Option<String>,
}

// ── Handlers ──────────────────────────────────────────────────────────────────

pub async fn run_analysis(
    State(mut state): State<AppState>,
    Json(req): Json<AnalysisRequest>,
) -> Result<(StatusCode, Json<AnalysisOut>)> {
    if req.career_path.is_none() && req.compare_programme_id.is_none() {
        return Err(AppError::BadRequest(
            "one of career_path or compare_programme_id must be set".into(),
        ));
    }

    let analysis = sqlx::query_as::<_, GapAnalysis>(
        r#"
        INSERT INTO gap_analyses (programme_id, career_path, compare_programme_id, scenario, status, created_at)
        VALUES ($1, $2, $3, $4, 'pending', $5)
        RETURNING id, programme_id, career_path, compare_programme_id, scenario,
                  status, celery_task_id, created_at, completed_at
        "#,
    )
    .bind(req.programme_id)
    .bind(&req.career_path)
    .bind(req.compare_programme_id)
    .bind(&req.scenario)
    .bind(Utc::now().naive_utc())
    .fetch_one(&state.pool)
    .await?;

    let task_id = queue::push_analysis(
        &mut state.analysis_queue,
        GapAnalysisJob { analysis_id: analysis.id },
    )
    .await
    .map_err(AppError::Internal)?;

    sqlx::query("UPDATE gap_analyses SET celery_task_id = $1 WHERE id = $2")
        .bind(&task_id)
        .bind(analysis.id)
        .execute(&state.pool)
        .await?;

    let mut out = AnalysisOut::from(analysis);
    out.celery_task_id = Some(task_id.clone());
    tracing::info!(analysis_id = out.id, task_id, "gap analysis enqueued");
    Ok((StatusCode::ACCEPTED, Json(out)))
}

pub async fn list_analyses(State(state): State<AppState>) -> Result<Json<Vec<AnalysisOut>>> {
    let rows = sqlx::query_as::<_, GapAnalysis>(
        "SELECT id, programme_id, career_path, compare_programme_id, scenario, status, celery_task_id, created_at, completed_at FROM gap_analyses ORDER BY created_at DESC"
    )
    .fetch_all(&state.pool)
    .await?;
    Ok(Json(rows.into_iter().map(AnalysisOut::from).collect()))
}

pub async fn get_analysis(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<AnalysisOut>> {
    let row = sqlx::query_as::<_, GapAnalysis>(
        "SELECT id, programme_id, career_path, compare_programme_id, scenario, status, celery_task_id, created_at, completed_at FROM gap_analyses WHERE id = $1"
    )
    .bind(id)
    .fetch_optional(&state.pool)
    .await?
    .ok_or(AppError::NotFound)?;
    Ok(Json(AnalysisOut::from(row)))
}

pub async fn analysis_status(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<AnalysisStatus>> {
    #[derive(sqlx::FromRow)]
    struct StatusRow {
        id: i32,
        status: String,
        celery_task_id: Option<String>,
    }

    let row = sqlx::query_as::<_, StatusRow>(
        "SELECT id, status, celery_task_id FROM gap_analyses WHERE id = $1"
    )
    .bind(id)
    .fetch_optional(&state.pool)
    .await?
    .ok_or(AppError::NotFound)?;

    Ok(Json(AnalysisStatus {
        analysis_id: row.id,
        status: row.status,
        celery_task_id: row.celery_task_id,
    }))
}
