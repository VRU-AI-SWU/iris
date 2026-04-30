"""
Report generator.
Produces narrative summaries (via LLM) and PDF reports (via WeasyPrint).
"""
import logging
import os
from string import Template

from pipeline.llm_client import generate_narrative as llm_generate

logger = logging.getLogger(__name__)

_NARRATIVE_PROMPT = Template("""
You are an academic curriculum analyst writing a report for a university department head.
Write a concise, plain-language summary (3–5 paragraphs) of the following skill gap analysis results.

Programme: $programme_name
Career path analysed: $career_path
Overall alignment score (cosine similarity): $cosine_similarity (1.0 = perfect match)
KL divergence (market‖programme): $kl_divergence (higher = larger gap)

Top skill deficits (skills the market demands that this programme under-teaches):
$top_deficits

Top skill surpluses (skills this programme emphasises but the market rarely demands):
$top_surpluses

Common skills (well covered by both programme and market):
$common_skills

Write the summary for a non-technical academic administrator. Be specific and actionable.
Do not use jargon. Mention the programme name and career path in the first sentence.
""")

_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  body { font-family: sans-serif; font-size: 12px; margin: 40px; color: #222; }
  h1 { font-size: 18px; color: #1a1a2e; }
  h2 { font-size: 14px; color: #333; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
  table { border-collapse: collapse; width: 100%; font-size: 11px; }
  th { background: #1a1a2e; color: white; padding: 6px; text-align: left; }
  td { padding: 5px; border-bottom: 1px solid #eee; }
  .deficit { color: #c0392b; }
  .surplus { color: #27ae60; }
  .score-box { background: #f4f4f4; padding: 10px; border-radius: 4px; margin: 10px 0; }
  .narrative { line-height: 1.6; margin: 16px 0; }
</style>
</head>
<body>
<h1>Iris — Skill Gap Analysis Report</h1>
<p><strong>Programme:</strong> {programme} &nbsp;|&nbsp;
   <strong>Career Path:</strong> {career_path} &nbsp;|&nbsp;
   <strong>Analysis ID:</strong> {analysis_id}</p>

<div class="score-box">
  <strong>KL Divergence (market‖programme):</strong> {kl:.4f} &nbsp;&nbsp;
  <strong>Cosine Similarity:</strong> {cos:.4f}
</div>

<h2>Summary</h2>
<div class="narrative">{narrative}</div>

<h2>Ranked Skill Gaps (Top 20)</h2>
<table>
  <tr><th>Skill</th><th>Market Weight</th><th>Programme Weight</th><th>Gap Score</th><th>Direction</th></tr>
  {gap_rows}
</table>
</body>
</html>
"""


def generate_narrative(
    programme_name: str,
    career_path: str,
    kl_divergence: float,
    cosine_similarity: float,
    top_deficits: list[dict],
    top_surpluses: list[dict],
    skill_decomposition: dict,
) -> str:
    """Generate plain-language narrative summary via LLM."""
    def fmt_skills(items):
        return "\n".join(f"  - {r['label']} (gap={r['gap_score']:.3f})" for r in items) or "  (none)"

    prompt = _NARRATIVE_PROMPT.substitute(
        programme_name=programme_name,
        career_path=career_path or "N/A",
        cosine_similarity=f"{cosine_similarity:.3f}",
        kl_divergence=f"{kl_divergence:.4f}",
        top_deficits=fmt_skills(top_deficits),
        top_surpluses=fmt_skills(top_surpluses),
        common_skills=", ".join((skill_decomposition or {}).get("common", [])[:10]) or "(none)",
    )
    return llm_generate(prompt)


def render_pdf(
    output_path: str,
    analysis_id: int,
    narrative: str,
    heatmap_data: dict,
    ranked_gaps: list[dict],
    kl_divergence: float,
    cosine_similarity: float,
    programme_name: str = "",
    career_path: str = "",
):
    """Render gap analysis results to a PDF file."""
    from weasyprint import HTML

    gap_rows = ""
    for row in (ranked_gaps or [])[:20]:
        css_class = row.get("direction", "")
        gap_rows += (
            f"<tr>"
            f"<td>{row.get('label', '')}</td>"
            f"<td>{row.get('market_weight', 0):.4f}</td>"
            f"<td>{row.get('programme_weight', 0):.4f}</td>"
            f"<td class='{css_class}'>{row.get('gap_score', 0):+.4f}</td>"
            f"<td class='{css_class}'>{css_class}</td>"
            f"</tr>"
        )

    html_content = _HTML_TEMPLATE.format(
        programme=programme_name or f"Programme {analysis_id}",
        career_path=career_path or "N/A",
        analysis_id=analysis_id,
        kl=kl_divergence or 0.0,
        cos=cosine_similarity or 0.0,
        narrative=narrative.replace("\n", "<br/>") if narrative else "",
        gap_rows=gap_rows,
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    HTML(string=html_content).write_pdf(output_path)
    logger.info("PDF report written to %s", output_path)
