use apalis::prelude::{Data, Error};
use shared::jobs::ScrapeJob;
use std::sync::Arc;

use crate::{
    pipeline::{llm_client::LlmClient, scraper},
    state::WorkerState,
};

pub async fn process(
    job: ScrapeJob,
    state: Data<Arc<WorkerState>>,
) -> Result<(), Error> {
    let pool = &(**state).pool;
    let settings = &(**state).settings;
    let http = &(**state).http;

    tracing::info!(
        career_path = %job.career_path,
        sources = ?job.sources,
        "scrape job started"
    );

    // Use the career_path string as the search query
    let query = job.career_path.replace('-', " ");

    let postings = scraper::run_scrapers(
        http,
        &job.career_path,
        &query,
        &job.sources,
        settings.scrape_delay_secs,
    )
    .await;

    tracing::info!(count = postings.len(), "postings collected, extracting skills");

    let client = LlmClient::new(
        &settings.model_server_url,
        &settings.model_api_key,
        &settings.extraction_model,
        &settings.embedding_model,
    );

    let mut tx = pool.begin().await.map_err(map_db)?;

    for posting in &postings {
        // Build text for skill extraction
        let mut parts: Vec<&str> = Vec::new();
        if let Some(d) = &posting.description {
            parts.push(d.as_str());
        }
        if let Some(r) = &posting.requirements {
            parts.push(r.as_str());
        }
        let text = parts.join("\n");

        // Upsert job posting
        sqlx::query(
            r#"
            INSERT INTO job_postings
                (id, source, title, company, description, requirements,
                 career_path, posted_date, scraped_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
            ON CONFLICT (id) DO NOTHING
            "#,
        )
        .bind(&posting.id)
        .bind(&posting.source)
        .bind(&posting.title)
        .bind(&posting.company)
        .bind(&posting.description)
        .bind(&posting.requirements)
        .bind(&posting.career_path)
        .bind(posting.posted_date)
        .execute(&mut *tx)
        .await
        .map_err(map_db)?;

        // Extract and insert skills
        if !text.is_empty() {
            let skills = client.extract_skills(&text, 3).await.unwrap_or_default();
            for skill in &skills {
                sqlx::query(
                    r#"
                    INSERT INTO job_skills (posting_id, skill_term, source)
                    VALUES ($1, $2, 'llm')
                    ON CONFLICT (posting_id, skill_term) DO NOTHING
                    "#,
                )
                .bind(&posting.id)
                .bind(skill)
                .execute(&mut *tx)
                .await
                .map_err(map_db)?;
            }
        }
    }

    tx.commit().await.map_err(map_db)?;

    tracing::info!(
        career_path = %job.career_path,
        postings = postings.len(),
        "scrape job complete"
    );
    Ok(())
}

fn map_db(e: sqlx::Error) -> Error {
    Error::Failed(Arc::new(Box::new(e)))
}
