use serde::{Deserialize, Serialize};

/// Triggered when a TQF curriculum PDF is uploaded.
/// Worker parses the PDF and extracts skills into the DB.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TqfExtractionJob {
    pub programme_id: i32,
    pub pdf_path: String,
}

/// Triggered when a gap analysis is requested.
/// Worker runs KL divergence + RCA and writes results.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GapAnalysisJob {
    pub analysis_id: i32,
}

/// Triggered to scrape job postings for a career path.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScrapeJob {
    pub career_path: String,
    pub sources: Vec<String>,
}

/// Triggered to generate a PDF report for a completed analysis.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReportJob {
    pub analysis_id: i32,
}
