"""
Jobthai.com scraper.

Jobthai is Thailand's largest job portal (confirmed in academic research:
phaphuangwittayakul-2018, chaiaroon-2025).
"""
import hashlib
import logging
import re
from datetime import date, datetime

from pipeline.scraper.base import BaseScraper

logger = logging.getLogger(__name__)

# Map Iris career path labels to Jobthai search keywords
CAREER_PATH_KEYWORDS = {
    "data-analyst": ["data analyst", "นักวิเคราะห์ข้อมูล"],
    "data-engineer": ["data engineer", "วิศวกรข้อมูล"],
    "software-engineer": ["software engineer", "วิศวกรซอฟต์แวร์"],
    "devops": ["devops", "site reliability"],
    "frontend-dev": ["frontend developer", "front-end developer"],
    "backend-dev": ["backend developer", "back-end developer"],
    "fullstack-dev": ["fullstack developer", "full stack developer"],
    "cloud": ["cloud engineer", "cloud architect"],
    "information-security": ["information security", "cybersecurity", "ความมั่นคงสารสนเทศ"],
    "mobile-dev": ["mobile developer", "android developer", "ios developer"],
    "database-admin": ["database administrator", "dba"],
    "network-engineer": ["network engineer", "วิศวกรเครือข่าย"],
    "business-analyst": ["business analyst", "นักวิเคราะห์ธุรกิจ"],
    "project-manager": ["project manager", "ผู้จัดการโครงการ"],
    "tester": ["software tester", "qa engineer", "quality assurance"],
    "ux-ui-designer": ["ux designer", "ui designer", "ux/ui"],
    "it-support": ["it support", "helpdesk"],
    "java-dev": ["java developer", "java programmer"],
    "dotnet-dev": [".net developer", "c# developer"],
    "web-developer": ["web developer", "นักพัฒนาเว็บ"],
}


class JobthaiScraper(BaseScraper):
    source_name = "jobthai"
    base_url = "https://www.jobthai.com"

    def _get_search_urls(self, career_path: str) -> list[str]:
        keywords = CAREER_PATH_KEYWORDS.get(career_path, [career_path.replace("-", " ")])
        urls = []
        for kw in keywords[:2]:  # limit to first 2 keywords per career path
            encoded = kw.replace(" ", "+")
            urls.append(f"{self.base_url}/en/jobs?q={encoded}&page=1")
            urls.append(f"{self.base_url}/en/jobs?q={encoded}&page=2")
        return urls

    def _scrape_page(self, url: str, career_path: str) -> list[dict]:
        soup = self._get(url)
        if not soup:
            return []

        postings = []
        job_cards = soup.select("div.job-list-item, article.job-card, div[class*='job-item']")

        for card in job_cards:
            try:
                posting = self._parse_card(card)
                if posting:
                    postings.append(posting)
            except Exception as e:
                logger.debug("Failed to parse card: %s", e)

        return postings

    def _parse_card(self, card) -> dict | None:
        title_el = card.select_one("h2, h3, .job-title, [class*='title']")
        company_el = card.select_one(".company-name, [class*='company']")
        link_el = card.select_one("a[href]")

        if not title_el:
            return None

        title = title_el.get_text(strip=True)
        company = company_el.get_text(strip=True) if company_el else ""
        href = link_el["href"] if link_el else ""

        posting_id = hashlib.md5(f"{title}{company}".encode()).hexdigest()[:12]

        description, requirements = "", ""
        if href:
            detail_url = href if href.startswith("http") else f"{self.base_url}{href}"
            description, requirements = self._scrape_detail(detail_url)

        return {
            "id": self._make_id(posting_id),
            "title": title,
            "company": company,
            "description": description,
            "requirements": requirements,
            "posted_date": None,
        }

    def _scrape_detail(self, url: str) -> tuple[str, str]:
        """Scrape job detail page for description and requirements."""
        import time
        time.sleep(self.delay)
        soup = self._get(url)
        if not soup:
            return "", ""

        description = ""
        requirements = ""

        desc_el = soup.select_one(".job-description, [class*='description'], #job-description")
        if desc_el:
            description = desc_el.get_text(separator=" ", strip=True)[:2000]

        req_el = soup.select_one(".job-requirement, [class*='requirement'], #job-requirement")
        if req_el:
            requirements = req_el.get_text(separator=" ", strip=True)[:1000]
        elif not requirements and description:
            # Some postings combine description + requirements
            requirements = description

        return description, requirements
