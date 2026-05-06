-- Iris initial schema
-- Ported from Alembic 0001_initial_schema.py

CREATE TABLE IF NOT EXISTS programmes (
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(255) NOT NULL,
    university        VARCHAR(255) NOT NULL,
    degree            VARCHAR(100),
    tqf_filename      VARCHAR(512),
    created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    extraction_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    extraction_error  TEXT,
    extracted_at      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skill_clusters (
    id      SERIAL PRIMARY KEY,
    label   VARCHAR(512) NOT NULL UNIQUE,
    version INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS skill_tokens (
    id             SERIAL PRIMARY KEY,
    raw_text       VARCHAR(512) NOT NULL,
    cluster_id     INTEGER REFERENCES skill_clusters(id),
    embedding_json TEXT
);

CREATE TABLE IF NOT EXISTS courses (
    id             SERIAL PRIMARY KEY,
    programme_id   INTEGER NOT NULL REFERENCES programmes(id) ON DELETE CASCADE,
    code           VARCHAR(20),
    name_th        VARCHAR(512),
    name_en        VARCHAR(512),
    description_th TEXT,
    description_en TEXT,
    credits        FLOAT NOT NULL DEFAULT 3.0,
    category       VARCHAR(20) NOT NULL DEFAULT 'major',
    updated_at     TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (programme_id, code)
);

CREATE TABLE IF NOT EXISTS course_skills (
    id         SERIAL PRIMARY KEY,
    course_id  INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    skill_term VARCHAR(512) NOT NULL,
    source     VARCHAR(20) NOT NULL DEFAULT 'llm',
    cluster_id INTEGER REFERENCES skill_clusters(id),
    UNIQUE (course_id, skill_term)
);

CREATE TABLE IF NOT EXISTS job_postings (
    id           VARCHAR(128) PRIMARY KEY,
    source       VARCHAR(64) NOT NULL,
    title        VARCHAR(512),
    company      VARCHAR(512),
    description  TEXT,
    requirements TEXT,
    career_path  VARCHAR(64),
    posted_date  DATE,
    scraped_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS job_skills (
    id         SERIAL PRIMARY KEY,
    posting_id VARCHAR(128) NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    skill_term VARCHAR(512) NOT NULL,
    source     VARCHAR(20) NOT NULL DEFAULT 'llm',
    cluster_id INTEGER REFERENCES skill_clusters(id),
    UNIQUE (posting_id, skill_term)
);

CREATE TABLE IF NOT EXISTS gap_analyses (
    id                   SERIAL PRIMARY KEY,
    programme_id         INTEGER NOT NULL REFERENCES programmes(id) ON DELETE CASCADE,
    career_path          VARCHAR(64),
    compare_programme_id INTEGER REFERENCES programmes(id),
    scenario             VARCHAR(64) NOT NULL DEFAULT 'core',
    status               VARCHAR(50) NOT NULL DEFAULT 'pending',
    celery_task_id       VARCHAR(255),
    created_at           TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at         TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gap_results (
    id                  SERIAL PRIMARY KEY,
    analysis_id         INTEGER NOT NULL UNIQUE REFERENCES gap_analyses(id) ON DELETE CASCADE,
    kl_divergence       FLOAT,
    cosine_similarity   FLOAT,
    ranked_gaps         JSONB,
    skill_decomposition JSONB,
    heatmap_data        JSONB,
    narrative_summary   TEXT,
    pdf_path            VARCHAR(512)
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS ix_courses_programme_id       ON courses(programme_id);
CREATE INDEX IF NOT EXISTS ix_course_skills_course_id    ON course_skills(course_id);
CREATE INDEX IF NOT EXISTS ix_course_skills_cluster_id   ON course_skills(cluster_id);
CREATE INDEX IF NOT EXISTS ix_job_postings_career_path   ON job_postings(career_path);
CREATE INDEX IF NOT EXISTS ix_job_postings_scraped_at    ON job_postings(scraped_at);
CREATE INDEX IF NOT EXISTS ix_job_skills_posting_id      ON job_skills(posting_id);
CREATE INDEX IF NOT EXISTS ix_job_skills_cluster_id      ON job_skills(cluster_id);
CREATE INDEX IF NOT EXISTS ix_gap_analyses_programme_id  ON gap_analyses(programme_id);
