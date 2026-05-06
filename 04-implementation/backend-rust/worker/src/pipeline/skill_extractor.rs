use crate::pipeline::{llm_client::LlmClient, tqf_parser::ParsedCourse};
use anyhow::Result;

/// Per-course skill extraction result.
#[derive(Debug)]
pub struct CourseSkillSet {
    pub course_code: Option<String>,
    pub category: String,
    pub credits: f64,
    pub skills: Vec<String>,
}

/// Build bilingual extraction text from a parsed course and call the LLM.
pub async fn extract_from_course(client: &LlmClient, course: &ParsedCourse) -> Result<Vec<String>> {
    let mut parts: Vec<String> = Vec::new();

    if let Some(name) = &course.name_th {
        parts.push(name.clone());
    }
    if let Some(name) = &course.name_en {
        parts.push(name.clone());
    }
    if let Some(desc) = &course.description_th {
        parts.push(desc.clone());
    }
    if let Some(desc) = &course.description_en {
        parts.push(desc.clone());
    }

    if parts.is_empty() {
        return Ok(vec![]);
    }

    let text = parts.join("\n");
    client.extract_skills(&text, 3).await
}

/// Extract skills from all courses, returning one `CourseSkillSet` per course.
/// Courses that yield no skills are still included (empty `skills` vec).
pub async fn batch_extract(client: &LlmClient, courses: &[ParsedCourse]) -> Vec<CourseSkillSet> {
    let mut results = Vec::with_capacity(courses.len());
    for course in courses {
        let skills = extract_from_course(client, course)
            .await
            .unwrap_or_default();
        results.push(CourseSkillSet {
            course_code: course.code.clone(),
            category: course.category.clone(),
            credits: course.credits,
            skills,
        });
    }
    results
}
