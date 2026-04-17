---
id: "003"
title: "Xây dựng TopCV scraper"
status: "in_progress"
area: "backend"
agent: "@builder"
priority: "high"
created_at: "2026-04-18"
due_date: null
started_at: "2026-04-18"
completed_at: null
prd_refs: ["FR-002", "FR-004", "FR-005"]
blocks: ["005"]
blocked_by: ["001"]
---

## Description

Xây dựng scraper cho TopCV.vn — một trong các trang việc làm lớn nhất Việt Nam với 3M+ monthly visits. Cấu trúc giống ITviecScraper, output cùng schema.

Output file: `data/raw/topcv_<YYYYMMDD_HHMMSS>.json`

## Acceptance Criteria

- [ ] File `src/scrapers/topcv.py` tồn tại với class `TopCVScraper`
- [ ] Thu thập được các fields: title, company, location, salary, description, url, posted_date, job_type, source="topcv"
- [ ] Xử lý phân trang, thu thập tối thiểu 500 tin
- [ ] Retry logic tối đa 3 lần, exponential backoff
- [ ] Gracefully skip tin bị lỗi
- [ ] Lưu output ra `data/raw/topcv_<timestamp>.json`
- [ ] Có thể chạy standalone
- [ ] Tests pass (mock HTTP, không gọi thật)

## History

| Date | Agent / Human | Event |
|------|--------------|-------|
| 2026-04-18 | human | Task created |
| 2026-04-18 | orchestrator | Task started, delegated to @builder |
