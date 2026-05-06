/// Scraper for jobthai.com
///
/// Search URL: https://www.jobthai.com/en/jobs?q={query}&page={n}
/// CSS selectors verified against site structure as of 2026-05.
use anyhow::Result;
use reqwest::Client;
use tokio::time::{sleep, Duration};

use super::common::{posting_id, ScrapedPosting};

const BASE: &str = "https://www.jobthai.com";
const MAX_PAGES: u32 = 5;

pub async fn scrape(
    http: &Client,
    career_path: &str,
    query: &str,
    delay_secs: f64,
) -> Result<Vec<ScrapedPosting>> {
    let mut postings = Vec::new();

    for page in 1..=MAX_PAGES {
        let url = format!("{BASE}/en/jobs?q={query}&page={page}");
        let html = fetch(http, &url).await?;

        // Parse in a sync scope — Html/ElementRef are !Send, must not cross await
        let page_postings: Vec<ScrapedPosting> = {
            use scraper::{Html, Selector};
            let doc = Html::parse_document(&html);
            let card_sel = Selector::parse("article.job-card, div.job-item").unwrap();
            let link_sel = Selector::parse("a[href]").unwrap();

            // Collect card HTML strings first (owned, Send)
            let card_htmls: Vec<(String, String)> = doc
                .select(&card_sel)
                .map(|card| {
                    let link = card
                        .select(&link_sel)
                        .next()
                        .and_then(|a| a.value().attr("href"))
                        .map(|h| {
                            if h.starts_with('/') {
                                format!("{BASE}{h}")
                            } else {
                                h.to_string()
                            }
                        })
                        .unwrap_or_else(|| url.clone());
                    (card.html(), link)
                })
                .collect();

            card_htmls
                .into_iter()
                .filter_map(|(card_html, link)| {
                    let card_doc = Html::parse_document(&card_html);
                    let title = super::common::select_text(
                        &card_doc,
                        "h2.job-title, .job-title a",
                    )?;
                    let company =
                        super::common::select_text(&card_doc, ".company-name, .employer-name");
                    let description = super::common::select_text(
                        &card_doc,
                        ".job-description, .job-detail",
                    );
                    Some(ScrapedPosting {
                        id: posting_id("jobthai", &link),
                        source: "jobthai".to_string(),
                        title,
                        company,
                        description,
                        requirements: None,
                        career_path: career_path.to_string(),
                        posted_date: None,
                    })
                })
                .collect()
        }; // doc and all scraper types dropped here

        if page_postings.is_empty() {
            break;
        }
        postings.extend(page_postings);
        sleep(Duration::from_secs_f64(delay_secs)).await;
    }

    tracing::info!(source = "jobthai", career_path, count = postings.len(), "scrape done");
    Ok(postings)
}

async fn fetch(http: &Client, url: &str) -> Result<String> {
    Ok(http
        .get(url)
        .header("Accept-Language", "th,en;q=0.9")
        .send()
        .await?
        .text()
        .await?)
}
