/// TQF (มคอ.2) PDF parser.
///
/// Extracts course list, descriptions, credit hours, and course category
/// (major / general education / free elective) from Thai TQF documents.
///
/// TQF category markers:
///   หมวดวิชาเฉพาะ       → major    (weight 1.0)
///   หมวดวิชาศึกษาทั่วไป  → general  (weight 0.5)
///   หมวดวิชาเลือกเสรี   → elective (weight 0.0 in core scenario)
use anyhow::{Context, Result};
use regex::Regex;
use std::path::Path;

// Thai-language category markers
const MAJOR_MARKERS: &[&str] = &["หมวดวิชาเฉพาะ", "วิชาเฉพาะ"];
const GENERAL_MARKERS: &[&str] = &[
    "หมวดวิชาศึกษาทั่วไป",
    "วิชาศึกษาทั่วไป",
    "วิชาการศึกษาทั่วไป",
];
const ELECTIVE_MARKERS: &[&str] = &["หมวดวิชาเลือกเสรี", "วิชาเลือกเสรี"];

#[derive(Debug, Clone)]
pub struct ParsedCourse {
    pub code: Option<String>,
    pub name_th: Option<String>,
    pub name_en: Option<String>,
    pub description_th: Option<String>,
    pub description_en: Option<String>,
    pub credits: f64,
    pub category: String, // "major" | "general" | "elective"
}

#[derive(Debug)]
pub struct ParsedProgramme {
    pub courses: Vec<ParsedCourse>,
}

/// Extract all courses from a TQF PDF.
/// Runs the blocking pdf-extract call inside spawn_blocking.
pub async fn parse_tqf_pdf(pdf_path: impl AsRef<Path> + Send + 'static) -> Result<ParsedProgramme> {
    let path = pdf_path.as_ref().to_path_buf();
    let text = tokio::task::spawn_blocking(move || {
        pdf_extract::extract_text(&path).context("pdf text extraction")
    })
    .await
    .context("spawn_blocking panicked")??;

    tracing::debug!(chars = text.len(), "PDF text extracted");
    let courses = extract_courses(&text);
    tracing::info!(count = courses.len(), "parsed courses from TQF PDF");
    Ok(ParsedProgramme { courses })
}

// ── Internal parsing ──────────────────────────────────────────────────────────

fn extract_courses(text: &str) -> Vec<ParsedCourse> {
    let mut courses = Vec::new();
    for (category, section) in split_by_category(text) {
        courses.extend(parse_course_descriptions(&section, &category));
    }
    courses
}

/// Split TQF full text into sections keyed by category.
fn split_by_category(text: &str) -> Vec<(String, String)> {
    let mut sections: Vec<(String, String)> = Vec::new();
    let mut current_category = "major".to_string();
    let mut current_lines: Vec<&str> = Vec::new();

    for line in text.lines() {
        let stripped = line.trim();

        let new_cat = if MAJOR_MARKERS.iter().any(|m| stripped.contains(m)) {
            Some("major")
        } else if GENERAL_MARKERS.iter().any(|m| stripped.contains(m)) {
            Some("general")
        } else if ELECTIVE_MARKERS.iter().any(|m| stripped.contains(m)) {
            Some("elective")
        } else {
            None
        };

        if let Some(cat) = new_cat {
            if !current_lines.is_empty() {
                sections.push((current_category.clone(), current_lines.join("\n")));
                current_lines.clear();
            }
            current_category = cat.to_string();
        }
        current_lines.push(line);
    }

    if !current_lines.is_empty() {
        sections.push((current_category, current_lines.join("\n")));
    }

    // No markers found — treat whole document as major
    if sections.is_empty() {
        sections.push(("major".to_string(), text.to_string()));
    }

    sections
}

/// Extract individual course blocks from a category section.
fn parse_course_descriptions(text: &str, category: &str) -> Vec<ParsedCourse> {
    // Match lines that start with a course code: 7–8 digits OR 2–4 upper letters + 3–6 digits
    let code_re = Regex::new(r"(?m)^(\d{7,8}|[A-Z]{2,4}\s?\d{3,6})\s+(.+)$").unwrap();
    let matches: Vec<_> = code_re.find_iter(text).collect();

    if matches.is_empty() {
        return parse_by_description_headers(text, category);
    }

    let mut courses = Vec::new();
    for (i, m) in matches.iter().enumerate() {
        let block_start = m.start();
        let block_end = matches.get(i + 1).map(|n| n.start()).unwrap_or(text.len());
        let block = text[block_start..block_end].trim();
        let course = parse_single_block(block, category);
        if course.description_th.is_some() || course.description_en.is_some() {
            courses.push(course);
        }
    }
    courses
}

/// Fallback: split on 'คำอธิบายรายวิชา' (course description header).
fn parse_by_description_headers(text: &str, category: &str) -> Vec<ParsedCourse> {
    let header = "คำอธิบายรายวิชา";
    text.split(header)
        .skip(1) // first chunk is pre-header
        .filter_map(|block| {
            let thai_lines: Vec<&str> = block
                .lines()
                .map(str::trim)
                .filter(|l| !l.is_empty() && is_thai(l))
                .collect();
            if thai_lines.is_empty() {
                return None;
            }
            Some(ParsedCourse {
                code: None,
                name_th: None,
                name_en: None,
                description_th: Some(thai_lines[..thai_lines.len().min(10)].join(" ")),
                description_en: None,
                credits: 3.0,
                category: category.to_string(),
            })
        })
        .collect()
}

/// Parse a single course text block.
fn parse_single_block(block: &str, category: &str) -> ParsedCourse {
    let credit_re = Regex::new(r"\b(\d+)\s*(?:\(\d+[-–]\d+[-–]\d+\)|\s*หน่วยกิต)").unwrap();
    let code_re = Regex::new(r"\b([A-Z]{2,4}\s?\d{3,6}|\d{7,8})\b").unwrap();

    let lines: Vec<&str> = block.lines().map(str::trim).filter(|l| !l.is_empty()).collect();

    let mut course = ParsedCourse {
        code: None,
        name_th: None,
        name_en: None,
        description_th: None,
        description_en: None,
        credits: 3.0,
        category: category.to_string(),
    };

    if lines.is_empty() {
        return course;
    }

    // Code from first line
    if let Some(m) = code_re.find(lines[0]) {
        course.code = Some(m.as_str().replace(' ', ""));
    }

    // Credits from whole block
    if let Some(m) = credit_re.captures(block) {
        if let Ok(c) = m[1].parse::<f64>() {
            course.credits = c;
        }
    }

    // Split remaining lines into Thai vs English
    let mut thai_lines: Vec<&str> = Vec::new();
    let mut eng_lines: Vec<&str> = Vec::new();
    for line in lines.iter().skip(1) {
        if is_thai(line) {
            thai_lines.push(line);
        } else if !line.is_empty() {
            eng_lines.push(line);
        }
    }

    if !thai_lines.is_empty() {
        course.name_th = Some(thai_lines[0].to_string());
        if thai_lines.len() > 1 {
            course.description_th = Some(thai_lines[1..].join(" "));
        }
    }

    // Filter out credit-notation-only English lines
    let non_credit_en: Vec<&str> = eng_lines
        .iter()
        .copied()
        .filter(|l| credit_re.find(l).is_none() || l.len() > 10)
        .collect();

    if !non_credit_en.is_empty() {
        course.name_en = Some(non_credit_en[0].to_string());
        if non_credit_en.len() > 1 {
            course.description_en = Some(non_credit_en[1..].join(" "));
        }
    }

    course
}

/// True if more than 20% of characters fall in the Thai Unicode block (U+0E00–U+0E7F).
pub fn is_thai(text: &str) -> bool {
    let chars: Vec<char> = text.chars().collect();
    if chars.is_empty() {
        return false;
    }
    let thai = chars.iter().filter(|&&c| c >= '\u{0E00}' && c <= '\u{0E7F}').count();
    thai as f64 / chars.len() as f64 > 0.2
}
