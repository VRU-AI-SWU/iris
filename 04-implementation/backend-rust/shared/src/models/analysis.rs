use chrono::NaiveDateTime;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use sqlx::FromRow;

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct GapAnalysis {
    pub id: i32,
    pub programme_id: i32,
    pub career_path: Option<String>,
    pub compare_programme_id: Option<i32>,
    pub scenario: String, // "core" | "core_electives" | "hypothetical"
    pub status: String,   // "pending" | "running" | "completed" | "failed"
    pub celery_task_id: Option<String>,
    pub created_at: NaiveDateTime,
    pub completed_at: Option<NaiveDateTime>,
}

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct GapResult {
    pub id: i32,
    pub analysis_id: i32,
    pub kl_divergence: Option<f64>,
    pub cosine_similarity: Option<f64>,
    pub ranked_gaps: Option<Value>,
    pub skill_decomposition: Option<Value>,
    pub heatmap_data: Option<Value>,
    pub narrative_summary: Option<String>,
    pub pdf_path: Option<String>,
}
