use apalis::prelude::Storage;
use apalis_redis::RedisStorage;
use shared::jobs::{GapAnalysisJob, ReportJob, ScrapeJob, TqfExtractionJob};

pub async fn push_tqf(
    storage: &mut RedisStorage<TqfExtractionJob>,
    job: TqfExtractionJob,
) -> anyhow::Result<String> {
    let parts = storage.push(job).await.map_err(|e| anyhow::anyhow!("{e}"))?;
    Ok(parts.task_id.to_string())
}

pub async fn push_analysis(
    storage: &mut RedisStorage<GapAnalysisJob>,
    job: GapAnalysisJob,
) -> anyhow::Result<String> {
    let parts = storage.push(job).await.map_err(|e| anyhow::anyhow!("{e}"))?;
    Ok(parts.task_id.to_string())
}

pub async fn push_scrape(
    storage: &mut RedisStorage<ScrapeJob>,
    job: ScrapeJob,
) -> anyhow::Result<String> {
    let parts = storage.push(job).await.map_err(|e| anyhow::anyhow!("{e}"))?;
    Ok(parts.task_id.to_string())
}

pub async fn push_report(
    storage: &mut RedisStorage<ReportJob>,
    job: ReportJob,
) -> anyhow::Result<String> {
    let parts = storage.push(job).await.map_err(|e| anyhow::anyhow!("{e}"))?;
    Ok(parts.task_id.to_string())
}
