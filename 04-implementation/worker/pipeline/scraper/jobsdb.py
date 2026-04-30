"""JobsDB Thailand scraper (placeholder — selectors to be validated against live site)."""
import hashlib
import logging

from pipeline.scraper.base import BaseScraper
from pipeline.scraper.jobthai import CAREER_PATH_KEYWORDS

logger = logging.getLogger(__name__)


class JobsdbScraper(BaseScraper):
    source_name = "jobsdb"
    base_url = "https://th.jobsdb.com"

    def _get_search_urls(self, career_path: str) -> list[str]:
        keywords = CAREER_PATH_KEYWORDS.get(career_path, [career_path.replace("-", " ")])
        urls = []
        for kw in keywords[:2]:
            encoded = kw.replace(" ", "-").lower()
            urls.append(f"{self.base_url}/jobs-in-thailand/{encoded}/1")
        return urls

    def _scrape_page(self, url: str, career_path: str) -> list[dict]:
        soup = self._get(url)
        if not soup:
            return []

        postings = []
        cards = soup.select("article[data-job-id], div[data-automation='jobCard']")
        for card in cards:
            try:
                posting = self._parse_card(card)
                if posting:
                    postings.append(posting)
            except Exception as e:
                logger.debug("JobsDB parse error: %s", e)
        return postings

    def _parse_card(self, card) -> dict | None:
        title_el = card.select_one("h1, h2, [data-automation='jobTitle']")
        company_el = card.select_one("[data-automation='jobCompany'], .company")
        if not title_el:
            return None

        title = title_el.get_text(strip=True)
        company = company_el.get_text(strip=True) if company_el else ""
        posting_id = hashlib.md5(f"{title}{company}".encode()).hexdigest()[:12]

        return {
            "id": self._make_id(posting_id),
            "title": title,
            "company": company,
            "description": "",
            "requirements": "",
            "posted_date": None,
        }
