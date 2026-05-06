use reqwest::Client;
use shared::config::Settings;
use sqlx::PgPool;
use std::sync::Arc;

/// Shared state for all job processors.
/// Wrapped in Arc so it can be cheaply cloned into each processor closure.
#[allow(dead_code)] // settings and http used from Sprint 4 onwards
pub struct WorkerState {
    pub pool: PgPool,
    pub settings: Settings,
    pub http: Client,
}

impl WorkerState {
    pub fn new(pool: PgPool, settings: Settings) -> Arc<Self> {
        Arc::new(Self {
            pool,
            settings,
            http: Client::builder()
                .user_agent("iris-worker/0.1")
                .build()
                .expect("failed to build HTTP client"),
        })
    }
}
