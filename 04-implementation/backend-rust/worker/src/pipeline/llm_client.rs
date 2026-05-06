use anyhow::{anyhow, Context, Result};
use async_openai::{
    config::OpenAIConfig,
    types::{
        ChatCompletionRequestUserMessageArgs, CreateChatCompletionRequestArgs,
        CreateEmbeddingRequestArgs,
    },
    Client,
};
use std::time::Duration;
use tokio::time::sleep;

pub struct LlmClient {
    client: Client<OpenAIConfig>,
    extraction_model: String,
    embedding_model: String,
}

impl LlmClient {
    pub fn new(base_url: &str, api_key: &str, extraction_model: &str, embedding_model: &str) -> Self {
        let config = OpenAIConfig::new()
            .with_api_base(base_url)
            .with_api_key(api_key);
        Self {
            client: Client::with_config(config),
            extraction_model: extraction_model.to_string(),
            embedding_model: embedding_model.to_string(),
        }
    }

    /// Extract skill terms from free text using zero-shot LLM prompt.
    /// Retries up to `retries` times with exponential back-off.
    pub async fn extract_skills(&self, text: &str, retries: u32) -> Result<Vec<String>> {
        let prompt = format!(
            "You are a skill extraction assistant. \
             Extract all technical skills, tools, programming languages, frameworks, \
             methodologies, and domain knowledge areas mentioned in the following text. \
             Return ONLY a JSON array of short skill strings (1–5 words each). \
             Do not include soft skills. If no skills are found, return [].\n\n\
             Text:\n{text}\n\nSkills (JSON array):"
        );

        let mut last_err = anyhow!("no attempts made");
        for attempt in 0..retries {
            match self.chat_once(&prompt, 0.0, 512).await {
                Ok(raw) => match parse_skill_json(&raw) {
                    Ok(skills) => return Ok(skills),
                    Err(e) => last_err = e,
                },
                Err(e) => last_err = e,
            }
            if attempt < retries - 1 {
                sleep(Duration::from_secs(2u64.pow(attempt))).await;
            }
        }
        tracing::warn!("skill extraction failed after {retries} attempts: {last_err}");
        Ok(vec![]) // degrade gracefully — return empty rather than failing the job
    }

    /// Embed a list of texts using the embedding model.
    pub async fn embed_texts(&self, texts: Vec<String>) -> Result<Vec<Vec<f32>>> {
        if texts.is_empty() {
            return Ok(vec![]);
        }
        let request = CreateEmbeddingRequestArgs::default()
            .model(&self.embedding_model)
            .input(texts)
            .build()
            .context("build embedding request")?;
        let response = self
            .client
            .embeddings()
            .create(request)
            .await
            .context("embedding API call")?;
        Ok(response.data.into_iter().map(|e| e.embedding).collect())
    }

    /// Generate a plain-language narrative summary.
    pub async fn generate_narrative(&self, prompt: &str, max_tokens: u16) -> Result<String> {
        self.chat_once(prompt, 0.3, max_tokens).await
    }

    // ── Internal ───────────────────────────────────────────────────────────────

    async fn chat_once(&self, prompt: &str, temperature: f32, max_tokens: u16) -> Result<String> {
        let msg = ChatCompletionRequestUserMessageArgs::default()
            .content(prompt)
            .build()
            .context("build chat message")?;

        let request = CreateChatCompletionRequestArgs::default()
            .model(&self.extraction_model)
            .messages(vec![msg.into()])
            .temperature(temperature)
            .max_tokens(max_tokens)
            .build()
            .context("build chat request")?;

        let response = self
            .client
            .chat()
            .create(request)
            .await
            .context("chat API call")?;

        let content = response
            .choices
            .into_iter()
            .next()
            .and_then(|c| c.message.content)
            .unwrap_or_default();

        Ok(content.trim().to_string())
    }
}

/// Parse the LLM response into a Vec<String>. Strips markdown fences.
fn parse_skill_json(raw: &str) -> Result<Vec<String>> {
    let cleaned = strip_markdown_fences(raw);
    let skills: Vec<serde_json::Value> =
        serde_json::from_str(cleaned.trim()).context("parse skill JSON")?;
    Ok(skills
        .into_iter()
        .filter_map(|v| v.as_str().map(|s| s.trim().to_string()))
        .filter(|s| !s.is_empty())
        .collect())
}

fn strip_markdown_fences(s: &str) -> &str {
    let s = s.trim();
    if let Some(rest) = s.strip_prefix("```") {
        // Skip optional language tag line (e.g. "json\n")
        let rest = rest.trim_start_matches(|c: char| c.is_alphabetic());
        let rest = rest.trim_start_matches('\n');
        if let Some(inner) = rest.strip_suffix("```") {
            return inner;
        }
    }
    s
}
