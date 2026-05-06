use chrono::NaiveDateTime;
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct Programme {
    pub id: i32,
    pub name: String,
    pub university: String,
    pub degree: Option<String>,
    pub tqf_filename: Option<String>,
    pub created_at: NaiveDateTime,
    pub extraction_status: String,
    pub extraction_error: Option<String>,
    pub extracted_at: Option<NaiveDateTime>,
}

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct Course {
    pub id: i32,
    pub programme_id: i32,
    pub code: Option<String>,
    pub name_th: Option<String>,
    pub name_en: Option<String>,
    pub description_th: Option<String>,
    pub description_en: Option<String>,
    pub credits: f64,
    pub category: String,
    pub updated_at: NaiveDateTime,
}

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct CourseSkill {
    pub id: i32,
    pub course_id: i32,
    pub skill_term: String,
    pub source: String,
    pub cluster_id: Option<i32>,
}
