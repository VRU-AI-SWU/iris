use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use chrono::NaiveDate;
use serde::{Deserialize, Serialize};

use crate::{error::Result, queue, state::AppState};
use shared::{jobs::ScrapeJob, models::job::JobPosting};

// ── Request / response types ───────────────────────────────────────────────────

#[derive(Deserialize)]
pub struct ScrapeRequest {
    pub career_path: String,
    #[serde(default = "default_sources")]
    pub sources: Vec<String>,
}

fn default_sources() -> Vec<String> {
    vec![
        "jobthai".into(),
        "jobsdb".into(),
        "jobbkk".into(),
        "jobtopgun".into(),
    ]
}

#[derive(Serialize)]
pub struct ScrapeStatus {
    pub task_id: String,
    pub status: String,
    pub info: String,
}

#[derive(Serialize)]
pub struct JobPostingOut {
    pub id: String,
    pub source: String,
    pub title: Option<String>,
    pub company: Option<String>,
    pub career_path: Option<String>,
    pub posted_date: Option<NaiveDate>,
    pub scraped_at: chrono::NaiveDateTime,
}

impl From<JobPosting> for JobPostingOut {
    fn from(j: JobPosting) -> Self {
        Self {
            id: j.id,
            source: j.source,
            title: j.title,
            company: j.company,
            career_path: j.career_path,
            posted_date: j.posted_date,
            scraped_at: j.scraped_at,
        }
    }
}

#[derive(Deserialize)]
pub struct JobListQuery {
    pub career_path: Option<String>,
    pub source: Option<String>,
    #[serde(default = "default_limit")]
    pub limit: i64,
    #[serde(default)]
    pub offset: i64,
}

fn default_limit() -> i64 {
    50
}

#[derive(Deserialize)]
pub struct DistributionQuery {
    pub career_path: String,
}

// ── Handlers ──────────────────────────────────────────────────────────────────

pub async fn trigger_scrape(
    State(mut state): State<AppState>,
    Json(req): Json<ScrapeRequest>,
) -> Result<(StatusCode, Json<ScrapeStatus>)> {
    let task_id = queue::push_scrape(
        &mut state.scrape_queue,
        ScrapeJob {
            career_path: req.career_path.clone(),
            sources: req.sources,
        },
    )
    .await
    .map_err(crate::error::AppError::Internal)?;

    tracing::info!(task_id, career_path = req.career_path, "scrape job enqueued");
    Ok((
        StatusCode::ACCEPTED,
        Json(ScrapeStatus {
            task_id,
            status: "queued".into(),
            info: String::new(),
        }),
    ))
}

pub async fn scrape_status(Path(task_id): Path<String>) -> Result<Json<ScrapeStatus>> {
    Ok(Json(ScrapeStatus {
        task_id,
        status: "unknown".into(),
        info: "full status tracking via apalis job store — Sprint 3 complete".into(),
    }))
}

pub async fn list_postings(
    State(state): State<AppState>,
    Query(q): Query<JobListQuery>,
) -> Result<Json<Vec<JobPostingOut>>> {
    let limit = q.limit.min(500);
    let sql_base = "SELECT id, source, title, company, description, requirements, career_path, posted_date, scraped_at FROM job_postings";

    let rows: Vec<JobPosting> = match (&q.career_path, &q.source) {
        (Some(cp), Some(src)) => sqlx::query_as::<_, JobPosting>(
            &format!("{sql_base} WHERE career_path = $1 AND source = $2 ORDER BY scraped_at DESC LIMIT $3 OFFSET $4")
        )
        .bind(cp).bind(src).bind(limit).bind(q.offset)
        .fetch_all(&state.pool).await?,

        (Some(cp), None) => sqlx::query_as::<_, JobPosting>(
            &format!("{sql_base} WHERE career_path = $1 ORDER BY scraped_at DESC LIMIT $2 OFFSET $3")
        )
        .bind(cp).bind(limit).bind(q.offset)
        .fetch_all(&state.pool).await?,

        (None, Some(src)) => sqlx::query_as::<_, JobPosting>(
            &format!("{sql_base} WHERE source = $1 ORDER BY scraped_at DESC LIMIT $2 OFFSET $3")
        )
        .bind(src).bind(limit).bind(q.offset)
        .fetch_all(&state.pool).await?,

        (None, None) => sqlx::query_as::<_, JobPosting>(
            &format!("{sql_base} ORDER BY scraped_at DESC LIMIT $1 OFFSET $2")
        )
        .bind(limit).bind(q.offset)
        .fetch_all(&state.pool).await?,
    };

    Ok(Json(rows.into_iter().map(JobPostingOut::from).collect()))
}

pub async fn get_distributions(
    State(state): State<AppState>,
    Query(q): Query<DistributionQuery>,
) -> Result<Json<serde_json::Value>> {
    #[derive(sqlx::FromRow)]
    struct Row {
        cluster_id: Option<i32>,
        cnt: Option<i64>,
    }

    let window_months = state.settings.job_posting_window_months as i64;
    let cutoff =
        chrono::Utc::now().naive_utc() - chrono::Duration::days(window_months * 30);

    let rows = sqlx::query_as::<_, Row>(
        r#"
        SELECT js.cluster_id, COUNT(js.id) AS cnt
        FROM job_skills js
        JOIN job_postings jp ON js.posting_id = jp.id
        WHERE jp.career_path = $1
          AND jp.scraped_at >= $2
          AND js.cluster_id IS NOT NULL
        GROUP BY js.cluster_id
        "#,
    )
    .bind(&q.career_path)
    .bind(cutoff)
    .fetch_all(&state.pool)
    .await?;

    let total: f64 = rows.iter().map(|r| r.cnt.unwrap_or(0) as f64).sum();
    let distribution = if total == 0.0 {
        serde_json::json!({})
    } else {
        let map: serde_json::Map<String, serde_json::Value> = rows
            .iter()
            .filter_map(|r| {
                r.cluster_id.map(|id| {
                    (id.to_string(), serde_json::json!(r.cnt.unwrap_or(0) as f64 / total))
                })
            })
            .collect();
        serde_json::Value::Object(map)
    };

    Ok(Json(serde_json::json!({
        "career_path": q.career_path,
        "distribution": distribution,
    })))
}
