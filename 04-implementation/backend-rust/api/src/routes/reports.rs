use axum::{
    body::Body,
    extract::{Path, State},
    http::{header, StatusCode},
    response::Response,
    Json,
};
use serde::Serialize;
use tokio::fs::File;
use tokio_util::io::ReaderStream;

use crate::{
    error::{AppError, Result},
    queue,
    state::AppState,
};
use shared::jobs::ReportJob;

#[derive(Serialize)]
pub struct ReportOut {
    pub analysis_id: i32,
    pub narrative_summary: Option<String>,
    pub heatmap_data: Option<serde_json::Value>,
    pub ranked_gaps: Option<serde_json::Value>,
}

pub async fn generate_report(
    State(mut state): State<AppState>,
    Path(analysis_id): Path<i32>,
) -> Result<(StatusCode, Json<serde_json::Value>)> {
    #[derive(sqlx::FromRow)]
    struct Row {
        status: String,
    }

    let row = sqlx::query_as::<_, Row>("SELECT status FROM gap_analyses WHERE id = $1")
        .bind(analysis_id)
        .fetch_optional(&state.pool)
        .await?
        .ok_or(AppError::NotFound)?;

    if row.status != "completed" {
        return Err(AppError::BadRequest("analysis not yet completed".into()));
    }

    let task_id = queue::push_report(
        &mut state.report_queue,
        ReportJob { analysis_id },
    )
    .await
    .map_err(AppError::Internal)?;

    tracing::info!(analysis_id, task_id, "report generation enqueued");
    Ok((
        StatusCode::ACCEPTED,
        Json(serde_json::json!({ "task_id": task_id, "status": "queued" })),
    ))
}

pub async fn get_report(
    State(state): State<AppState>,
    Path(analysis_id): Path<i32>,
) -> Result<Json<ReportOut>> {
    #[derive(sqlx::FromRow)]
    struct Row {
        narrative_summary: Option<String>,
        heatmap_data: Option<serde_json::Value>,
        ranked_gaps: Option<serde_json::Value>,
    }

    let row = sqlx::query_as::<_, Row>(
        "SELECT gr.narrative_summary, gr.heatmap_data, gr.ranked_gaps FROM gap_results gr WHERE gr.analysis_id = $1"
    )
    .bind(analysis_id)
    .fetch_optional(&state.pool)
    .await?
    .ok_or(AppError::NotFound)?;

    Ok(Json(ReportOut {
        analysis_id,
        narrative_summary: row.narrative_summary,
        heatmap_data: row.heatmap_data,
        ranked_gaps: row.ranked_gaps,
    }))
}

pub async fn download_pdf(
    State(state): State<AppState>,
    Path(analysis_id): Path<i32>,
) -> Result<Response> {
    #[derive(sqlx::FromRow)]
    struct Row {
        pdf_path: Option<String>,
    }

    let row = sqlx::query_as::<_, Row>(
        "SELECT gr.pdf_path FROM gap_results gr WHERE gr.analysis_id = $1"
    )
    .bind(analysis_id)
    .fetch_optional(&state.pool)
    .await?
    .ok_or(AppError::NotFound)?;

    let pdf_path = row.pdf_path.ok_or(AppError::NotFound)?;
    let file = File::open(&pdf_path).await.map_err(|_| AppError::NotFound)?;
    let stream = ReaderStream::new(file);
    let filename = format!("iris-report-{analysis_id}.pdf");

    let response = Response::builder()
        .status(StatusCode::OK)
        .header(header::CONTENT_TYPE, "application/pdf")
        .header(
            header::CONTENT_DISPOSITION,
            format!("attachment; filename=\"{filename}\""),
        )
        .body(Body::from_stream(stream))
        .map_err(|e| AppError::Internal(anyhow::anyhow!(e)))?;

    Ok(response)
}
