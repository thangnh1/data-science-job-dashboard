"""Tests for src/scrapers/itviec.py.

All HTTP calls are mocked via the ``responses`` library — no real network
traffic is made during the test suite.
"""

import json
from pathlib import Path

import responses as responses_lib
from requests.exceptions import ConnectionError as RequestsConnectionError

from src.scrapers.itviec import ITviecScraper

# ---------------------------------------------------------------------------
# Fixture HTML helpers
# ---------------------------------------------------------------------------

_BASE_URL = "https://itviec.com/it-jobs"


def _make_job_card(
    *,
    title: str = "Senior Python Developer",
    company: str = "Acme Corp",
    location: str = "TP.HCM",
    salary: str | None = "20-30 triệu",
    description: str = "Build scalable backend services.",
    url: str = "/senior-python-developer-acme-1234",
    posted_date: str = "3 ngày trước",
    job_type: str = "Full-time",
) -> str:
    """Return an HTML snippet representing a single ITviec job card."""
    salary_html = f'<div class="job-card__salary">{salary}</div>' if salary else ""
    return f"""
    <div class="job-card">
        <h3 class="job-card__title">
            <a href="{url}">{title}</a>
        </h3>
        <div class="job-card__company">
            <a href="/company/acme">{company}</a>
        </div>
        <div class="job-card__location">{location}</div>
        {salary_html}
        <div class="job-card__description">{description}</div>
        <span class="job-card__posted-date">{posted_date}</span>
        <span class="job-card__type">{job_type}</span>
    </div>
    """


def _wrap_page(cards_html: str, has_next: bool = False) -> str:
    """Wrap one or more card HTML snippets in a minimal page shell."""
    next_link = (
        '<a href="/it-jobs?page=2" aria-label="Next">Next</a>' if has_next else ""
    )
    return f"""
    <html><body>
        <div id="job-list">
            {cards_html}
        </div>
        <nav class="pagination">{next_link}</nav>
    </body></html>
    """


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_scraper_instantiation() -> None:
    """ITviecScraper() creates instance with correct defaults."""
    scraper = ITviecScraper()
    assert scraper.max_pages == 20
    assert scraper.delay == 1.5
    assert scraper.BASE_URL == "https://itviec.com/it-jobs"


@responses_lib.activate
def test_parse_job_fields() -> None:
    """Given a mock HTML page with one job card, all required fields are present."""
    page_html = _wrap_page(_make_job_card())
    responses_lib.add(responses_lib.GET, _BASE_URL, body=page_html, status=200)

    scraper = ITviecScraper(max_pages=1, delay=0)
    jobs = scraper.scrape()

    assert len(jobs) == 1
    job = jobs[0]

    required_keys = {
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
    assert required_keys == set(
        job.keys()
    ), f"Missing keys: {required_keys - set(job.keys())}"

    assert job["title"] == "Senior Python Developer"
    assert job["company"] == "Acme Corp"
    assert job["location"] == "TP.HCM"
    assert job["salary"] == "20-30 triệu"
    assert job["description"] == "Build scalable backend services."
    assert job["url"].startswith("https://itviec.com")
    assert job["posted_date"] == "3 ngày trước"
    assert job["job_type"] == "Full-time"
    assert job["source"] == "itviec"
    assert job["scraped_at"]  # non-empty ISO timestamp


@responses_lib.activate
def test_missing_salary_is_none() -> None:
    """Job cards without a salary element return None for the salary field."""
    page_html = _wrap_page(_make_job_card(salary=None))
    responses_lib.add(responses_lib.GET, _BASE_URL, body=page_html, status=200)

    scraper = ITviecScraper(max_pages=1, delay=0)
    jobs = scraper.scrape()

    assert len(jobs) == 1
    assert jobs[0]["salary"] is None


def test_save_creates_json_file(tmp_path: Path) -> None:
    """save() writes a valid JSON file to the given output directory."""
    scraper = ITviecScraper()
    sample_jobs = [
        {
            "title": "Backend Developer",
            "company": "Tech Co",
            "location": "Hà Nội",
            "salary": "15-25 triệu",
            "description": "Work on APIs.",
            "url": "https://itviec.com/backend-dev-123",
            "posted_date": "1 ngày trước",
            "job_type": "Full-time",
            "source": "itviec",
            "scraped_at": "2026-04-18T00:00:00+00:00",
        }
    ]

    output_path = scraper.save(sample_jobs, output_dir=str(tmp_path))

    saved_file = Path(output_path)
    assert saved_file.exists(), "Output file was not created."
    assert saved_file.suffix == ".json"
    assert saved_file.name.startswith("itviec_")

    with saved_file.open(encoding="utf-8") as fh:
        loaded = json.load(fh)

    assert loaded == sample_jobs


@responses_lib.activate
def test_retry_on_network_error() -> None:
    """Scraper retries on RequestException and succeeds on the third attempt."""
    page_html = _wrap_page(_make_job_card())

    # First two requests raise a connection error; third succeeds.
    responses_lib.add(
        responses_lib.GET,
        _BASE_URL,
        body=RequestsConnectionError("Connection refused"),
    )
    responses_lib.add(
        responses_lib.GET,
        _BASE_URL,
        body=RequestsConnectionError("Connection refused"),
    )
    responses_lib.add(responses_lib.GET, _BASE_URL, body=page_html, status=200)

    scraper = ITviecScraper(max_pages=1, delay=0)
    # Patch backoff sleep so the test runs fast.
    import unittest.mock as mock

    with mock.patch("src.scrapers.itviec.time.sleep"):
        jobs = scraper.scrape()

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Senior Python Developer"


@responses_lib.activate
def test_graceful_skip_on_bad_job() -> None:
    """If one job card fails to parse, the remaining cards are still returned."""
    good_card = _make_job_card(title="Good Job", company="Good Corp")
    # A malformed card — completely empty div that will produce None for title/company
    bad_card = "<div class='job-card'></div>"

    page_html = _wrap_page(good_card + bad_card)
    responses_lib.add(responses_lib.GET, _BASE_URL, body=page_html, status=200)

    # Patch _parse_card so the second card always raises an exception
    original_parse = ITviecScraper._parse_card
    call_count = 0

    def patched_parse(self, card, scraped_at):
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise ValueError("Simulated parse failure on card 2")
        return original_parse(self, card, scraped_at)

    import unittest.mock as mock

    with mock.patch.object(ITviecScraper, "_parse_card", patched_parse):
        scraper = ITviecScraper(max_pages=1, delay=0)
        jobs = scraper.scrape()

    # One card succeeded, one was skipped gracefully
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Good Job"


@responses_lib.activate
def test_pagination_stops_when_no_next_page() -> None:
    """Scraper stops after the first page when no next-page link is present."""
    page_html = _wrap_page(_make_job_card(), has_next=False)
    responses_lib.add(responses_lib.GET, _BASE_URL, body=page_html, status=200)

    scraper = ITviecScraper(max_pages=5, delay=0)
    jobs = scraper.scrape()

    # Only one page should have been fetched
    assert len(responses_lib.calls) == 1
    assert len(jobs) == 1


@responses_lib.activate
def test_pagination_follows_next_page() -> None:
    """Scraper follows the next-page link when present."""
    page1_html = _wrap_page(_make_job_card(title="Job Page 1"), has_next=True)
    page2_html = _wrap_page(_make_job_card(title="Job Page 2"), has_next=False)

    responses_lib.add(responses_lib.GET, _BASE_URL, body=page1_html, status=200)
    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}?page=2",
        body=page2_html,
        status=200,
    )

    scraper = ITviecScraper(max_pages=5, delay=0)
    import unittest.mock as mock

    with mock.patch("src.scrapers.itviec.time.sleep"):
        jobs = scraper.scrape()

    assert len(jobs) == 2
    titles = {j["title"] for j in jobs}
    assert "Job Page 1" in titles
    assert "Job Page 2" in titles


@responses_lib.activate
def test_all_retries_exhausted_returns_empty() -> None:
    """When all retry attempts fail, scrape() returns an empty list."""
    responses_lib.add(
        responses_lib.GET,
        _BASE_URL,
        body=RequestsConnectionError("Timeout"),
    )
    responses_lib.add(
        responses_lib.GET,
        _BASE_URL,
        body=RequestsConnectionError("Timeout"),
    )
    responses_lib.add(
        responses_lib.GET,
        _BASE_URL,
        body=RequestsConnectionError("Timeout"),
    )

    scraper = ITviecScraper(max_pages=1, delay=0)
    import unittest.mock as mock

    with mock.patch("src.scrapers.itviec.time.sleep"):
        jobs = scraper.scrape()

    assert jobs == []


def test_save_creates_output_directory(tmp_path: Path) -> None:
    """save() creates the output directory if it does not exist."""
    scraper = ITviecScraper()
    nested_dir = tmp_path / "nested" / "subdir"
    assert not nested_dir.exists()

    output_path = scraper.save([], output_dir=str(nested_dir))

    assert nested_dir.exists()
    assert Path(output_path).exists()
