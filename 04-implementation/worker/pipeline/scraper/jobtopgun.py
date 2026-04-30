"""JOBTOPGUN.com scraper (placeholder — selectors to be validated against live site)."""
import hashlib
import logging

from pipeline.scraper.base import BaseScraper
from pipeline.scraper.jobthai import CAREER_PATH_KEYWORDS

logger = logging.getLogger(__name__)


class JobtopgunScraper(BaseScraper):
    source_name = "jobtopgun"
    base_url = "https://www.jobtopgun.com"

    def _get_search_urls(self, career_path: str) -> list[str]:
        keywords = CAREER_PATH_KEYWORDS.get(career_path, [career_path.replace("-", " ")])
        return [f"{self.base_url}/jobs?q={kw.replace(' ', '+')}" for kw in keywords[:2]]

    def _scrape_page(self, url: str, career_path: str) -> list[dict]:
        soup = self._get(url)
        if not soup:
            return []
        cards = soup.select(".job-card, .job-item, article")
        postings = []
        for card in cards:
            title_el = card.select_one("h2, h3, .job-title, a")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            company_el = card.select_one(".company, .employer")
            company = company_el.get_text(strip=True) if company_el else ""
            posting_id = hashlib.md5(f"{title}{company}".encode()).hexdigest()[:12]
            postings.append({
                "id": self._make_id(posting_id),
                "title": title,
                "company": company,
                "description": "",
                "requirements": "",
                "posted_date": None,
            })
        return postings
