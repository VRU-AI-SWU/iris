pub mod common;
pub mod jobbkk;
pub mod jobsdb;
pub mod jobthai;
pub mod jobtopgun;

use anyhow::Result;
use reqwest::Client;

use common::ScrapedPosting;

/// Dispatch to the appropriate scraper(s) based on the source list.
/// Unknown source names are silently skipped.
pub async fn run_scrapers(
    http: &Client,
    career_path: &str,
    query: &str,
    sources: &[String],
    delay_secs: f64,
) -> Vec<ScrapedPosting> {
    let mut all: Vec<ScrapedPosting> = Vec::new();

    for source in sources {
        let result: Result<Vec<ScrapedPosting>> = match source.as_str() {
            "jobthai" => jobthai::scrape(http, career_path, query, delay_secs).await,
            "jobsdb"  => jobsdb::scrape(http, career_path, query, delay_secs).await,
            "jobbkk"  => jobbkk::scrape(http, career_path, query, delay_secs).await,
            "jobtopgun" => jobtopgun::scrape(http, career_path, query, delay_secs).await,
            other => {
                tracing::warn!(source = other, "unknown scrape source, skipping");
                continue;
            }
        };

        match result {
            Ok(postings) => all.extend(postings),
            Err(e) => tracing::error!(source = %source, error = %e, "scrape failed"),
        }
    }

    // Deduplicate by ID in case the same posting appears on multiple pages
    all.sort_by(|a, b| a.id.cmp(&b.id));
    all.dedup_by_key(|p| p.id.clone());
    all
}
