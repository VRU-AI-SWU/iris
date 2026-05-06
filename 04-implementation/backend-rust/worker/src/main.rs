mod jobs;
mod pipeline;
mod state;

use apalis::prelude::*;
use apalis_redis::RedisStorage;
use shared::{
    config::Settings,
    db,
    jobs::{GapAnalysisJob, ReportJob, ScrapeJob, TqfExtractionJob},
};
use state::WorkerState;
use tracing::info;
use tracing_subscriber::{fmt, prelude::*, EnvFilter};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    dotenvy::dotenv().ok();

    let settings = Settings::from_env()?;

    tracing_subscriber::registry()
        .with(EnvFilter::new(&settings.log_level))
        .with(fmt::layer())
        .init();

    let pool = db::create_pool(&settings.database_url).await?;
    db::health_check(&pool).await?;
    info!("Database connection established");

    let redis_conn = apalis_redis::connect(settings.redis_url.clone()).await?;
    info!("Redis connection established");

    let worker_state = WorkerState::new(pool, settings);

    // One RedisStorage per job type — each uses a dedicated Redis key namespace
    let tqf_storage      = RedisStorage::<TqfExtractionJob>::new(redis_conn.clone());
    let analysis_storage = RedisStorage::<GapAnalysisJob>::new(redis_conn.clone());
    let scrape_storage   = RedisStorage::<ScrapeJob>::new(redis_conn.clone());
    let report_storage   = RedisStorage::<ReportJob>::new(redis_conn);

    let tqf_worker = WorkerBuilder::new("iris-tqf")
        .data(worker_state.clone())
        .backend(tqf_storage)
        .build_fn(jobs::tqf_job::process);

    let analysis_worker = WorkerBuilder::new("iris-analysis")
        .data(worker_state.clone())
        .backend(analysis_storage)
        .build_fn(jobs::analysis_job::process);

    let scrape_worker = WorkerBuilder::new("iris-scrape")
        .data(worker_state.clone())
        .backend(scrape_storage)
        .build_fn(jobs::scrape_job::process);

    let report_worker = WorkerBuilder::new("iris-report")
        .data(worker_state.clone())
        .backend(report_storage)
        .build_fn(jobs::report_job::process);

    info!("Starting Iris worker — 4 job processors registered");

    Monitor::new()
        .register(tqf_worker)
        .register(analysis_worker)
        .register(scrape_worker)
        .register(report_worker)
        .run()
        .await?;

    Ok(())
}
