use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct SkillCluster {
    pub id: i32,
    pub label: String,
    pub version: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct SkillToken {
    pub id: i32,
    pub raw_text: String,
    pub cluster_id: Option<i32>,
    pub embedding_json: Option<String>,
}
