use apalis::prelude::{Data, Error};
use shared::jobs::TqfExtractionJob;
use std::sync::Arc;

use crate::{
    pipeline::{llm_client::LlmClient, skill_extractor, tqf_parser},
    state::WorkerState,
};

pub async fn process(
    job: TqfExtractionJob,
    state: Data<Arc<WorkerState>>,
) -> Result<(), Error> {
    let pool = &(**state).pool;
    let settings = &(**state).settings;

    tracing::info!(
        programme_id = job.programme_id,
        pdf_path = %job.pdf_path,
        "TQF extraction job started"
    );

    sqlx::query("UPDATE programmes SET extraction_status = 'running' WHERE id = $1")
        .bind(job.programme_id)
        .execute(pool)
        .await
        .map_err(map_db)?;

    let parsed = match tqf_parser::parse_tqf_pdf(job.pdf_path.clone()).await {
        Ok(p) => p,
        Err(e) => {
            let msg = e.to_string();
            fail_programme(pool, job.programme_id, &msg).await;
            let io_err = std::io::Error::new(std::io::ErrorKind::Other, msg);
            return Err(Error::Failed(Arc::new(Box::new(io_err))));
        }
    };

    let client = LlmClient::new(
        &settings.model_server_url,
        &settings.model_api_key,
        &settings.extraction_model,
        &settings.embedding_model,
    );

    let skill_sets = skill_extractor::batch_extract(&client, &parsed.courses).await;

    let mut tx = pool.begin().await.map_err(map_db)?;

    for (course, skill_set) in parsed.courses.iter().zip(skill_sets.iter()) {
        // Courses without a code use plain INSERT (NULL doesn't match UNIQUE)
        let course_id: i32 = if course.code.is_some() {
            sqlx::query_scalar(
                r#"
                INSERT INTO courses
                    (programme_id, code, name_th, name_en,
                     description_th, description_en, credits, category)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (programme_id, code)
                DO UPDATE SET
                    name_th        = EXCLUDED.name_th,
                    name_en        = EXCLUDED.name_en,
                    description_th = EXCLUDED.description_th,
                    description_en = EXCLUDED.description_en,
                    credits        = EXCLUDED.credits,
                    category       = EXCLUDED.category,
                    updated_at     = NOW()
                RETURNING id
                "#,
            )
            .bind(job.programme_id)
            .bind(&course.code)
            .bind(&course.name_th)
            .bind(&course.name_en)
            .bind(&course.description_th)
            .bind(&course.description_en)
            .bind(course.credits)
            .bind(&course.category)
            .fetch_one(&mut *tx)
            .await
            .map_err(map_db)?
        } else {
            sqlx::query_scalar(
                r#"
                INSERT INTO courses
                    (programme_id, code, name_th, name_en,
                     description_th, description_en, credits, category)
                VALUES ($1, NULL, $2, $3, $4, $5, $6, $7)
                RETURNING id
                "#,
            )
            .bind(job.programme_id)
            .bind(&course.name_th)
            .bind(&course.name_en)
            .bind(&course.description_th)
            .bind(&course.description_en)
            .bind(course.credits)
            .bind(&course.category)
            .fetch_one(&mut *tx)
            .await
            .map_err(map_db)?
        };

        for skill in &skill_set.skills {
            sqlx::query(
                r#"
                INSERT INTO course_skills (course_id, skill_term, source)
                VALUES ($1, $2, 'llm')
                ON CONFLICT (course_id, skill_term) DO NOTHING
                "#,
            )
            .bind(course_id)
            .bind(skill)
            .execute(&mut *tx)
            .await
            .map_err(map_db)?;
        }
    }

    tx.commit().await.map_err(map_db)?;

    sqlx::query(
        "UPDATE programmes SET extraction_status = 'done', extracted_at = NOW() WHERE id = $1",
    )
    .bind(job.programme_id)
    .execute(pool)
    .await
    .map_err(map_db)?;

    tracing::info!(
        programme_id = job.programme_id,
        courses = parsed.courses.len(),
        "TQF extraction complete"
    );
    Ok(())
}

fn map_db(e: sqlx::Error) -> Error {
    Error::Failed(Arc::new(Box::new(e)))
}

async fn fail_programme(pool: &sqlx::PgPool, id: i32, reason: &str) {
    let _ = sqlx::query(
        "UPDATE programmes SET extraction_status = 'failed', extraction_error = $2 WHERE id = $1",
    )
    .bind(id)
    .bind(reason)
    .execute(pool)
    .await;
}
