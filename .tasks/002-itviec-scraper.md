---
id: "002"
title: "Xây dựng ITviec scraper"
status: "in_progress"
area: "backend"
agent: "@builder"
priority: "high"
created_at: "2026-04-18"
due_date: null
started_at: "2026-04-18"
completed_at: null
prd_refs: ["FR-001", "FR-004", "FR-005"]
blocks: ["005"]
blocked_by: ["001"]
---

## Description

Xây dựng scraper cho ITviec.com — trang việc làm IT chuyên biệt lớn nhất Việt Nam. Scraper phải thu thập danh sách tin tuyển dụng IT, xử lý phân trang, và lưu dữ liệu thô ra JSON với timestamp.

Output file: `data/raw/itviec_<YYYYMMDD_HHMMSS>.json`

## Acceptance Criteria

- [ ] File `src/scrapers/itviec.py` tồn tại với class `ITviecScraper`
- [ ] Thu thập được các fields: title, company, location, salary (raw string), description, url, posted_date, job_type, source="itviec"
- [ ] Xử lý phân trang, thu thập tối thiểu 500 tin mỗi lần chạy
- [ ] Retry logic tối đa 3 lần khi gặp lỗi network
- [ ] Gracefully skip tin bị lỗi (không crash toàn bộ pipeline)
- [ ] Lưu output ra `data/raw/itviec_<timestamp>.json`
- [ ] Có thể chạy standalone: `python src/scrapers/itviec.py`
- [ ] Unit test `tests/test_scraper.py` với fixture data (không gọi HTTP thật)
- [ ] Tests pass

## Technical Notes

- ITviec dùng server-side rendering, có thể dùng requests + BeautifulSoup
- Base URL: https://itviec.com/it-jobs
- Dùng `requests.Session` với headers User-Agent hợp lệ
- Rate limiting: sleep 1-2s giữa các request
- Dùng `logging` module, không dùng `print()`
- Mock HTTP trong tests bằng `responses` library hoặc `pytest-httpx`

## History

| Date | Agent / Human | Event |
|------|--------------|-------|
| 2026-04-18 | human | Task created |
| 2026-04-18 | orchestrator | Task started, delegated to @builder |
