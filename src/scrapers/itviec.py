"""ITviec.com scraper for Vietnamese IT job listings.

Scrapes job postings from ITviec (Vietnam's largest IT-focused job board),
extracting title, company, location, salary, description, and metadata.
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

_REQUIRED_FIELDS = {
    "title",
    "company",
    "location",
    "salary",
    "description",
    "url",
    "posted_date",
    "job_type",
    "source",
    "scraped_at",
}


class ITviecScraper:
    """Scraper for ITviec.com IT job listings.

    Args:
        max_pages: Maximum number of listing pages to scrape.
        delay: Seconds to sleep between page requests.
    """

    BASE_URL = "https://itviec.com/it-jobs"

    def __init__(self, max_pages: int = 20, delay: float = 1.5) -> None:
        self.max_pages = max_pages
        self.delay = delay
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": _USER_AGENT})

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scrape(self) -> list[dict]:
        """Scrape job listings from ITviec across all pages.

        Returns:
            List of job dicts, each containing the required fields.
        """
        all_jobs: list[dict] = []
        scraped_at = datetime.now(timezone.utc).isoformat()

        for page in range(1, self.max_pages + 1):
            url = self._page_url(page)
            logger.info("Fetching page %d: %s", page, url)

            html = self._fetch_with_retry(url)
            if html is None:
                logger.warning(
                    "Failed to fetch page %d after retries — stopping.", page
                )
                break

            soup = BeautifulSoup(html, "html.parser")
            job_cards = self._find_job_cards(soup)

            if not job_cards:
                logger.info(
                    "No job cards found on page %d — stopping pagination.", page
                )
                break

            logger.info("Found %d job cards on page %d.", len(job_cards), page)

            for card in job_cards:
                try:
                    job = self._parse_card(card, scraped_at)
                    all_jobs.append(job)
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Skipping job card due to parse error: %s", exc)

            if not self._has_next_page(soup, page):
                logger.info("No next page detected after page %d — done.", page)
                break

            time.sleep(self.delay)

        logger.info("Scraping complete. Total jobs collected: %d", len(all_jobs))
        return all_jobs

    def save(self, jobs: list[dict], output_dir: str = "data/raw") -> str:
        """Persist jobs list to a timestamped JSON file.

        Args:
            jobs: List of job dicts returned by :meth:`scrape`.
            output_dir: Directory path (relative or absolute) to write the file.

        Returns:
            Absolute path of the written file.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = out_path / f"itviec_{timestamp}.json"

        with filename.open("w", encoding="utf-8") as fh:
            json.dump(jobs, fh, ensure_ascii=False, indent=2)

        logger.info("Saved %d jobs to %s", len(jobs), filename)
        return str(filename.resolve())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _page_url(self, page: int) -> str:
        """Build the URL for a given page number."""
        if page == 1:
            return self.BASE_URL
        return f"{self.BASE_URL}?page={page}"

    def _fetch_with_retry(
        self,
        url: str,
        max_retries: int = 3,
    ) -> str | None:
        """Fetch a URL with exponential-backoff retry on network errors.

        Args:
            url: The URL to GET.
            max_retries: Number of retry attempts before giving up.

        Returns:
            Response text on success, or None after exhausting retries.
        """
        backoff = 1.0
        for attempt in range(1, max_retries + 1):
            try:
                response = self._session.get(url, timeout=15)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as exc:
                logger.warning(
                    "Request error on attempt %d/%d for %s: %s",
                    attempt,
                    max_retries,
                    url,
                    exc,
                )
                if attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2
        return None

    def _find_job_cards(self, soup: BeautifulSoup) -> list:
        """Extract individual job card elements from a listing page.

        ITviec renders each job as an <div> with class ``job-card`` nested
        inside a container. The selectors here reflect ITviec's known layout
        as of early 2024 and fall back gracefully when the structure changes.
        """
        # Primary selector — ITviec job cards
        cards = soup.select("div.job-card")
        if cards:
            return cards

        # Fallback: some page variants use a <li> structure
        cards = soup.select("li.job-card")
        if cards:
            return cards

        # Broader fallback: any element carrying data-job-id attribute
        cards = soup.find_all(attrs={"data-job-id": True})
        if cards:
            return cards

        logger.warning("Could not locate job cards with any known selector.")
        return []

    def _parse_card(self, card, scraped_at: str) -> dict:
        """Parse a single job card element into a job dict.

        Args:
            card: A BeautifulSoup tag representing one job card.
            scraped_at: ISO 8601 timestamp string to embed in the record.

        Returns:
            A dict with all required job fields.
        """
        title = self._text(
            card.select_one(
                "h3.job-card__title a, h2.job-card__title a, a.job-title, h3 a"
            )
        )

        company = self._text(
            card.select_one(
                "div.job-card__company a, a.company-name,"
                " span.company-name, div.company a"
            )
        )

        location = self._text(
            card.select_one(
                "div.job-card__location, span.location, div.location, span.city"
            )
        )

        salary = self._text(
            card.select_one(
                "div.job-card__salary, span.salary, div.salary-range, span.salary-range"
            )
        )

        description = self._text(
            card.select_one(
                "div.job-card__description, div.job-description, p.description"
            )
        )

        # Job URL — prefer anchor inside title, fall back to any card-level anchor
        url = self._href(
            card.select_one("h3.job-card__title a, h2.job-card__title a, a.job-title")
        )

        posted_date = self._text(
            card.select_one(
                "span.job-card__posted-date, span.posted-at, time, span.time"
            )
        )
        # <time datetime="..."> carries a machine-readable value
        time_tag = card.select_one("time")
        if time_tag and not posted_date:
            posted_date = time_tag.get("datetime") or self._text(time_tag)

        job_type = self._text(
            card.select_one(
                "span.job-card__type, span.job-type, div.job-type, span.label-type"
            )
        )

        return {
            "title": title,
            "company": company,
            "location": location,
            "salary": salary if salary else None,
            "description": description,
            "url": self._absolute_url(url),
            "posted_date": posted_date if posted_date else None,
            "job_type": job_type if job_type else None,
            "source": "itviec",
            "scraped_at": scraped_at,
        }

    def _has_next_page(self, soup: BeautifulSoup, current_page: int) -> bool:
        """Determine whether a subsequent page of results exists.

        Checks for a pagination element pointing to page current_page + 1.
        """
        next_page_str = str(current_page + 1)

        # Look for a link whose href contains page=<next>
        for anchor in soup.select("a[href*='page=']"):
            href = anchor.get("href", "")
            if f"page={next_page_str}" in href:
                return True

        # Some themes use rel="next"
        if soup.select_one("a[rel='next']"):
            return True

        # Active/disabled next-button via aria-label
        next_btn = soup.select_one("a[aria-label='Next']")
        if next_btn and "disabled" not in next_btn.get("class", []):
            return True

        return False

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _text(tag) -> str | None:
        """Return stripped inner text of a tag, or None if tag is missing."""
        if tag is None:
            return None
        text = tag.get_text(separator=" ", strip=True)
        return text if text else None

    def _href(self, tag) -> str | None:
        """Return the href attribute of a tag, or None."""
        if tag is None:
            return None
        return tag.get("href")

    def _absolute_url(self, path: str | None) -> str | None:
        """Convert a relative path to an absolute ITviec URL."""
        if path is None:
            return None
        if path.startswith("http"):
            return path
        base = "https://itviec.com"
        return f"{base}/{path.lstrip('/')}"


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    scraper = ITviecScraper(max_pages=5, delay=2.0)
    jobs = scraper.scrape()
    if jobs:
        path = scraper.save(jobs)
        logger.info("Output written to %s", path)
    else:
        logger.warning("No jobs scraped.")
