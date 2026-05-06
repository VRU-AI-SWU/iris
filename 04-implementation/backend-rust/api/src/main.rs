mod error;
mod queue;
mod routes;
mod state;

use axum::{
    routing::{delete, get, post},
    Json, Router,
};
use apalis_redis::RedisStorage;
use serde_json::{json, Value};
use shared::{config::Settings, db};
use state::AppState;
use tower_http::cors::{Any, CorsLayer};
use tower_http::trace::TraceLayer;
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

    // Database
    let pool = db::create_pool(&settings.database_url).await?;
    db::health_check(&pool).await?;
    info!("Database connection established");

    sqlx::migrate!("../migrations")
        .run(&pool)
        .await
        .map_err(|e| anyhow::anyhow!("migration failed: {e}"))?;
    info!("Database migrations applied");

    // Redis job queues — one storage per job type
    let redis_conn = apalis_redis::connect(settings.redis_url.clone()).await?;
    let tqf_queue    = RedisStorage::new(redis_conn.clone());
    let analysis_queue = RedisStorage::new(redis_conn.clone());
    let scrape_queue = RedisStorage::new(redis_conn.clone());
    let report_queue = RedisStorage::new(redis_conn);
    info!("Redis job queues ready");

    let app_state = AppState {
        pool,
        settings: settings.clone(),
        tqf_queue,
        analysis_queue,
        scrape_queue,
        report_queue,
    };

    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = Router::new()
        .route("/health", get(health))
        // Programmes
        .route("/programmes", post(routes::programmes::upload_programme))
        .route("/programmes", get(routes::programmes::list_programmes))
        .route("/programmes/:id", get(routes::programmes::get_programme))
        .route("/programmes/:id", delete(routes::programmes::delete_programme))
        .route("/programmes/:id/courses", get(routes::programmes::get_courses))
        // Analysis
        .route("/analysis/run", post(routes::analysis::run_analysis))
        .route("/analysis", get(routes::analysis::list_analyses))
        .route("/analysis/:id", get(routes::analysis::get_analysis))
        .route("/analysis/:id/status", get(routes::analysis::analysis_status))
        // Jobs
        .route("/jobs/scrape", post(routes::jobs::trigger_scrape))
        .route("/jobs/scrape/:task_id", get(routes::jobs::scrape_status))
        .route("/jobs", get(routes::jobs::list_postings))
        .route("/jobs/distributions", get(routes::jobs::get_distributions))
        // Reports
        .route("/reports/generate/:id", post(routes::reports::generate_report))
        .route("/reports/:id", get(routes::reports::get_report))
        .route("/reports/:id/pdf", get(routes::reports::download_pdf))
        .layer(cors)
        .layer(TraceLayer::new_for_http())
        .with_state(app_state);

    let addr = "0.0.0.0:8000";
    info!("Iris API listening on {addr}");
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    Ok(())
}

async fn health() -> Json<Value> {
    Json(json!({ "status": "ok", "version": "0.1.0" }))
}
