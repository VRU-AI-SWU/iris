"""
Base scraper class for Thai job posting platforms.

All platform scrapers inherit from BaseScraper and implement:
  - scrape(career_path: str) → list[dict]

Each returned dict follows the unified job posting schema:
  {
    id: str           — unique identifier (source + posting ID)
    title: str
    company: str
    description: str
    requirements: str
    posted_date: date | None
  }
"""
import hashlib
import logging
import os
import time
from abc import ABC, abstractmethod
from datetime import date

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; IrisResearchBot/1.0; "
        "+https://github.com/VRU-AI-SWU/iris)"
    ),
    "Accept-Language": "th-TH,th;q=0.9,en;q=0.8",
}


class BaseScraper(ABC):
    source_name: str = "base"
    base_url: str = ""

    def __init__(self):
        self.delay = float(os.getenv("SCRAPE_DELAY", "2.0"))
        self.client = httpx.Client(headers=DEFAULT_HEADERS, timeout=30, follow_redirects=True)

    def scrape(self, career_path: str) -> list[dict]:
        """
        Scrape job postings for a career path.
        Subclasses implement _get_search_url and _parse_posting.
        """
        results = []
        urls = self._get_search_urls(career_path)

        for url in urls:
            try:
                postings = self._scrape_page(url, career_path)
                results.extend(postings)
                time.sleep(self.delay)
            except Exception as e:
                logger.warning("%s: failed to scrape %s — %s", self.source_name, url, e)

        logger.info("%s: scraped %d postings for %s", self.source_name, len(results), career_path)
        return results

    @abstractmethod
    def _get_search_urls(self, career_path: str) -> list[str]:
        """Return list of search result URLs for the given career path."""

    @abstractmethod
    def _scrape_page(self, url: str, career_path: str) -> list[dict]:
        """Scrape a single search result page and return list of posting dicts."""

    def _get(self, url: str) -> BeautifulSoup | None:
        """HTTP GET with error handling, returns parsed BeautifulSoup or None."""
        try:
            response = self.client.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except httpx.HTTPError as e:
            logger.warning("%s: HTTP error for %s — %s", self.source_name, url, e)
            return None

    def _make_id(self, posting_specific_id: str) -> str:
        return f"{self.source_name}_{posting_specific_id}"

    def __del__(self):
        self.client.close()
