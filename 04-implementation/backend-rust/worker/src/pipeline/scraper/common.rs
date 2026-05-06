use chrono::NaiveDate;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

/// Normalised posting struct returned by every site scraper.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScrapedPosting {
    /// Stable ID derived from source + URL so re-scraping is idempotent.
    pub id: String,
    pub source: String,
    pub title: String,
    pub company: Option<String>,
    pub description: Option<String>,
    pub requirements: Option<String>,
    pub career_path: String,
    pub posted_date: Option<NaiveDate>,
}

/// Derive a stable ID by hashing source + canonical URL.
pub fn posting_id(source: &str, url: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(source.as_bytes());
    hasher.update(url.as_bytes());
    format!("{:.16x}", hasher.finalize())
}

/// Extract inner text from a CSS selector, trimmed.
pub fn select_text(doc: &scraper::Html, selector: &str) -> Option<String> {
    let sel = scraper::Selector::parse(selector).ok()?;
    let text: String = doc
        .select(&sel)
        .next()?
        .text()
        .collect::<Vec<_>>()
        .join(" ")
        .trim()
        .to_string();
    if text.is_empty() { None } else { Some(text) }
}

/// Extract all matching elements' text, joined by newline.
pub fn select_all_text(doc: &scraper::Html, selector: &str) -> Option<String> {
    let sel = scraper::Selector::parse(selector).ok()?;
    let texts: Vec<String> = doc
        .select(&sel)
        .map(|el| el.text().collect::<Vec<_>>().join(" ").trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();
    if texts.is_empty() { None } else { Some(texts.join("\n")) }
}
