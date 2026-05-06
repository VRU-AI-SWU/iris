use std::env;

#[derive(Debug, Clone)]
pub struct Settings {
    pub model_server_url: String,
    pub model_api_key: String,
    pub extraction_model: String,
    pub embedding_model: String,

    pub database_url: String,
    pub redis_url: String,

    pub secret_key: String,
    pub debug: bool,
    pub log_level: String,

    pub scrape_delay_secs: f64,
    pub scrape_concurrency: usize,
    pub job_posting_window_months: u32,

    pub sidecar_url: String,
    pub upload_dir: String,
    pub reports_dir: String,
}

impl Settings {
    pub fn from_env() -> anyhow::Result<Self> {
        Ok(Self {
            model_server_url: env_str("MODEL_SERVER_URL", "http://host.docker.internal:1234/v1"),
            model_api_key: env_str("MODEL_API_KEY", "lm-studio"),
            extraction_model: env_str("EXTRACTION_MODEL", "gemma-4-31b-it"),
            embedding_model: env_str("EMBEDDING_MODEL", "text-embedding-embeddinggemma-300m"),

            database_url: env_required("DATABASE_URL")?,
            redis_url: env_str("REDIS_URL", "redis://redis:6379/0"),

            secret_key: env_str("SECRET_KEY", "change-me"),
            debug: env_str("DEBUG", "false").to_lowercase() == "true",
            log_level: env_str("LOG_LEVEL", "INFO"),

            scrape_delay_secs: env_str("SCRAPE_DELAY", "2.0").parse().unwrap_or(2.0),
            scrape_concurrency: env_str("SCRAPE_CONCURRENCY", "2").parse().unwrap_or(2),
            job_posting_window_months: env_str("JOB_POSTING_WINDOW_MONTHS", "12")
                .parse()
                .unwrap_or(12),

            sidecar_url: env_str("SIDECAR_URL", "http://cluster-sidecar:8002"),
            upload_dir: env_str("UPLOAD_DIR", "/app/data/tqf"),
            reports_dir: env_str("REPORTS_DIR", "/app/data/reports"),
        })
    }
}

fn env_str(key: &str, default: &str) -> String {
    env::var(key).unwrap_or_else(|_| default.to_string())
}

fn env_required(key: &str) -> anyhow::Result<String> {
    env::var(key).map_err(|_| anyhow::anyhow!("Required env var '{}' is not set", key))
}
