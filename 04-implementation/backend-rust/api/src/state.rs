use apalis_redis::RedisStorage;
use shared::{
    config::Settings,
    jobs::{GapAnalysisJob, ReportJob, ScrapeJob, TqfExtractionJob},
};
use sqlx::PgPool;

/// Shared state cloned into every Axum handler.
/// RedisStorage<T> is Clone (wraps a ConnectionManager Arc), so each handler
/// gets its own handle and can call push(&mut self) safely.
#[derive(Clone)]
pub struct AppState {
    pub pool: PgPool,
    pub settings: Settings,
    pub tqf_queue: RedisStorage<TqfExtractionJob>,
    pub analysis_queue: RedisStorage<GapAnalysisJob>,
    pub scrape_queue: RedisStorage<ScrapeJob>,
    pub report_queue: RedisStorage<ReportJob>,
}
