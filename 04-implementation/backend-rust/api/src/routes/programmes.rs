use axum::{
    extract::{Multipart, Path, State},
    http::StatusCode,
    Json,
};
use chrono::Utc;
use serde::Serialize;
use std::{fs, path::PathBuf};
use uuid::Uuid;

use crate::{
    error::{AppError, Result},
    queue,
    state::AppState,
};
use shared::{
    jobs::TqfExtractionJob,
    models::programme::{Course, Programme},
};

// ── Response types ─────────────────────────────────────────────────────────────

#[derive(Serialize)]
pub struct CourseOut {
    pub id: i32,
    pub code: Option<String>,
    pub name_th: Option<String>,
    pub name_en: Option<String>,
    pub credits: f64,
    pub category: String,
}

impl From<Course> for CourseOut {
    fn from(c: Course) -> Self {
        Self {
            id: c.id,
            code: c.code,
            name_th: c.name_th,
            name_en: c.name_en,
            credits: c.credits,
            category: c.category,
        }
    }
}

#[derive(Serialize)]
pub struct ProgrammeOut {
    pub id: i32,
    pub name: String,
    pub university: String,
    pub tqf_filename: Option<String>,
    pub extraction_status: String,
    pub created_at: chrono::NaiveDateTime,
}

impl From<Programme> for ProgrammeOut {
    fn from(p: Programme) -> Self {
        Self {
            id: p.id,
            name: p.name,
            university: p.university,
            tqf_filename: p.tqf_filename,
            extraction_status: p.extraction_status,
            created_at: p.created_at,
        }
    }
}

// ── Handlers ──────────────────────────────────────────────────────────────────

pub async fn upload_programme(
    State(mut state): State<AppState>,
    mut multipart: Multipart,
) -> Result<(StatusCode, Json<ProgrammeOut>)> {
    let mut name: Option<String> = None;
    let mut university: Option<String> = None;
    let mut file_bytes: Option<Vec<u8>> = None;
    let mut original_filename: Option<String> = None;

    while let Some(field) = multipart
        .next_field()
        .await
        .map_err(|e| AppError::BadRequest(format!("multipart error: {e}")))?
    {
        match field.name() {
            Some("name") => {
                name = Some(field.text().await.map_err(|e| AppError::BadRequest(e.to_string()))?);
            }
            Some("university") => {
                university =
                    Some(field.text().await.map_err(|e| AppError::BadRequest(e.to_string()))?);
            }
            Some("file") => {
                let fname = field
                    .file_name()
                    .ok_or_else(|| AppError::BadRequest("missing filename".into()))?
                    .to_string();
                if !fname.ends_with(".pdf") {
                    return Err(AppError::BadRequest("only PDF files accepted".into()));
                }
                original_filename = Some(fname);
                file_bytes = Some(
                    field
                        .bytes()
                        .await
                        .map_err(|e| AppError::BadRequest(e.to_string()))?
                        .to_vec(),
                );
            }
            _ => {}
        }
    }

    let name = name.ok_or_else(|| AppError::BadRequest("missing field: name".into()))?;
    let university =
        university.ok_or_else(|| AppError::BadRequest("missing field: university".into()))?;
    let bytes = file_bytes.ok_or_else(|| AppError::BadRequest("missing field: file".into()))?;
    let orig_name = original_filename.unwrap_or_else(|| "upload.pdf".into());

    let upload_dir = &state.settings.upload_dir;
    fs::create_dir_all(upload_dir)?;
    let filename = format!("{}_{orig_name}", Uuid::new_v4());
    let filepath = PathBuf::from(upload_dir).join(&filename);
    fs::write(&filepath, &bytes)?;

    let programme = sqlx::query_as::<_, Programme>(
        r#"
        INSERT INTO programmes (name, university, tqf_filename, created_at, extraction_status)
        VALUES ($1, $2, $3, $4, 'queued')
        RETURNING id, name, university, degree, tqf_filename, created_at, extraction_status
        "#,
    )
    .bind(&name)
    .bind(&university)
    .bind(&filename)
    .bind(Utc::now().naive_utc())
    .fetch_one(&state.pool)
    .await?;

    let task_id = queue::push_tqf(
        &mut state.tqf_queue,
        TqfExtractionJob {
            programme_id: programme.id,
            pdf_path: filepath.to_string_lossy().into_owned(),
        },
    )
    .await
    .map_err(AppError::Internal)?;

    tracing::info!(programme_id = programme.id, task_id, "TQF extraction enqueued");
    Ok((StatusCode::CREATED, Json(ProgrammeOut::from(programme))))
}

pub async fn list_programmes(State(state): State<AppState>) -> Result<Json<Vec<ProgrammeOut>>> {
    let rows = sqlx::query_as::<_, Programme>(
        "SELECT id, name, university, degree, tqf_filename, created_at, extraction_status FROM programmes ORDER BY created_at DESC"
    )
    .fetch_all(&state.pool)
    .await?;
    Ok(Json(rows.into_iter().map(ProgrammeOut::from).collect()))
}

pub async fn get_programme(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<ProgrammeOut>> {
    let row = sqlx::query_as::<_, Programme>(
        "SELECT id, name, university, degree, tqf_filename, created_at, extraction_status FROM programmes WHERE id = $1"
    )
    .bind(id)
    .fetch_optional(&state.pool)
    .await?
    .ok_or(AppError::NotFound)?;
    Ok(Json(ProgrammeOut::from(row)))
}

pub async fn get_courses(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<Vec<CourseOut>>> {
    let exists: bool = sqlx::query_scalar::<_, bool>(
        "SELECT EXISTS(SELECT 1 FROM programmes WHERE id = $1)"
    )
    .bind(id)
    .fetch_one(&state.pool)
    .await?;

    if !exists {
        return Err(AppError::NotFound);
    }

    let rows = sqlx::query_as::<_, Course>(
        "SELECT id, programme_id, code, name_th, name_en, description_th, description_en, credits, category FROM courses WHERE programme_id = $1 ORDER BY id"
    )
    .bind(id)
    .fetch_all(&state.pool)
    .await?;
    Ok(Json(rows.into_iter().map(CourseOut::from).collect()))
}

pub async fn delete_programme(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<StatusCode> {
    let result = sqlx::query("DELETE FROM programmes WHERE id = $1")
        .bind(id)
        .execute(&state.pool)
        .await?;
    if result.rows_affected() == 0 {
        return Err(AppError::NotFound);
    }
    Ok(StatusCode::NO_CONTENT)
}
