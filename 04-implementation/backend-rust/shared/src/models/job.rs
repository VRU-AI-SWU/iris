use chrono::{NaiveDate, NaiveDateTime};
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

// chaiaroon-2025 validated 20-role Thai digital taxonomy
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, sqlx::Type)]
#[sqlx(type_name = "varchar")]
pub enum CareerPath {
    #[serde(rename = "dotnet-dev")]
    DotnetDev,
    #[serde(rename = "backend-dev")]
    BackendDev,
    #[serde(rename = "business-analyst")]
    BusinessAnalyst,
    #[serde(rename = "cloud")]
    Cloud,
    #[serde(rename = "data-analyst")]
    DataAnalyst,
    #[serde(rename = "data-engineer")]
    DataEngineer,
    #[serde(rename = "database-admin")]
    DatabaseAdmin,
    #[serde(rename = "devops")]
    Devops,
    #[serde(rename = "frontend-dev")]
    FrontendDev,
    #[serde(rename = "fullstack-dev")]
    FullstackDev,
    #[serde(rename = "information-security")]
    InformationSecurity,
    #[serde(rename = "it-support")]
    ItSupport,
    #[serde(rename = "java-dev")]
    JavaDev,
    #[serde(rename = "mobile-dev")]
    MobileDev,
    #[serde(rename = "network-engineer")]
    NetworkEngineer,
    #[serde(rename = "project-manager")]
    ProjectManager,
    #[serde(rename = "software-engineer")]
    SoftwareEngineer,
    #[serde(rename = "tester")]
    Tester,
    #[serde(rename = "ux-ui-designer")]
    UxUiDesigner,
    #[serde(rename = "web-developer")]
    WebDeveloper,
}

impl CareerPath {
    pub fn as_str(&self) -> &'static str {
        match self {
            CareerPath::DotnetDev => "dotnet-dev",
            CareerPath::BackendDev => "backend-dev",
            CareerPath::BusinessAnalyst => "business-analyst",
            CareerPath::Cloud => "cloud",
            CareerPath::DataAnalyst => "data-analyst",
            CareerPath::DataEngineer => "data-engineer",
            CareerPath::DatabaseAdmin => "database-admin",
            CareerPath::Devops => "devops",
            CareerPath::FrontendDev => "frontend-dev",
            CareerPath::FullstackDev => "fullstack-dev",
            CareerPath::InformationSecurity => "information-security",
            CareerPath::ItSupport => "it-support",
            CareerPath::JavaDev => "java-dev",
            CareerPath::MobileDev => "mobile-dev",
            CareerPath::NetworkEngineer => "network-engineer",
            CareerPath::ProjectManager => "project-manager",
            CareerPath::SoftwareEngineer => "software-engineer",
            CareerPath::Tester => "tester",
            CareerPath::UxUiDesigner => "ux-ui-designer",
            CareerPath::WebDeveloper => "web-developer",
        }
    }

    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "dotnet-dev" => Some(CareerPath::DotnetDev),
            "backend-dev" => Some(CareerPath::BackendDev),
            "business-analyst" => Some(CareerPath::BusinessAnalyst),
            "cloud" => Some(CareerPath::Cloud),
            "data-analyst" => Some(CareerPath::DataAnalyst),
            "data-engineer" => Some(CareerPath::DataEngineer),
            "database-admin" => Some(CareerPath::DatabaseAdmin),
            "devops" => Some(CareerPath::Devops),
            "frontend-dev" => Some(CareerPath::FrontendDev),
            "fullstack-dev" => Some(CareerPath::FullstackDev),
            "information-security" => Some(CareerPath::InformationSecurity),
            "it-support" => Some(CareerPath::ItSupport),
            "java-dev" => Some(CareerPath::JavaDev),
            "mobile-dev" => Some(CareerPath::MobileDev),
            "network-engineer" => Some(CareerPath::NetworkEngineer),
            "project-manager" => Some(CareerPath::ProjectManager),
            "software-engineer" => Some(CareerPath::SoftwareEngineer),
            "tester" => Some(CareerPath::Tester),
            "ux-ui-designer" => Some(CareerPath::UxUiDesigner),
            "web-developer" => Some(CareerPath::WebDeveloper),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct JobPosting {
    pub id: String, // String(128) PK
    pub source: String,
    pub title: Option<String>,
    pub company: Option<String>,
    pub description: Option<String>,
    pub requirements: Option<String>,
    pub career_path: Option<String>,
    pub posted_date: Option<NaiveDate>,
    pub scraped_at: NaiveDateTime,
}

#[derive(Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct JobSkill {
    pub id: i32,
    pub posting_id: String,
    pub skill_term: String,
    pub source: String,
    pub cluster_id: Option<i32>,
}
