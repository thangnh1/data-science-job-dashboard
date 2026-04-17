# VN Tech Job Market Dashboard

Phân tích thị trường việc làm IT Việt Nam dựa trên dữ liệu thực tế từ 6 trang tuyển dụng lớn nhất.

> Inspired by [andresvourakis/ai-ds-job-market](https://github.com/andresvourakis/ai-ds-job-market) — rebuilt for the Vietnamese market.

---

## Tính năng

- **Kỹ năng hot nhất** — Top skills được yêu cầu nhiều nhất, filter theo category / địa điểm / seniority
- **Phân tích lương** — Phân phối lương theo role, seniority, thành phố; salary premium theo kỹ năng
- **Phân tích địa điểm** — So sánh Hà Nội vs TP.HCM vs Đà Nẵng vs Remote
- **AI/GenAI impact** — Tỷ lệ JD đề cập AI, trend theo tháng, salary premium cho AI skills
- **Job Explorer** — Search & filter tin tuyển dụng, highlight kỹ năng trong JD
- **Company Rankings** — Top công ty tuyển dụng nhiều nhất, kỹ năng & lương theo công ty

## Nguồn dữ liệu

| Nguồn | Đặc điểm |
|-------|----------|
| [ITviec](https://itviec.com) | IT-only, chất lượng cao |
| [TopCV](https://topcv.vn) | Lớn nhất VN, 3M+ visits/tháng |
| [VietnamWorks](https://vietnamworks.com) | Lâu đời nhất, enterprise |
| [Glints](https://glints.com/vn) | Startup & công ty nước ngoài |
| [Vieclam24h](https://vieclam24h.vn) | Entry-level & fresher |
| [123job](https://123job.vn) | SME & mid-market |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Data | Pandas, Plotly |
| Scraping | Requests, BeautifulSoup4 |
| Storage | SQLite |
| Package manager | Poetry |
| Python | 3.11+ |

---

## Cài đặt

### Dùng Poetry (khuyến nghị)

```bash
git clone https://github.com/thangnh1/data-science-job-dashboard
cd data-science-job-dashboard
poetry install
```

### Dùng pip

```bash
pip install -r requirements.txt
```

---

## Sử dụng

### 1. Thu thập dữ liệu

```bash
# Chạy tất cả scrapers
poetry run python src/scrapers/run_all.py

# Hoặc từng nguồn riêng
poetry run python src/scrapers/itviec.py
poetry run python src/scrapers/topcv.py
poetry run python src/scrapers/vietnamworks.py
```

Dữ liệu thô lưu tại `data/raw/` dưới dạng JSON có timestamp.

### 2. Xử lý dữ liệu

```bash
poetry run python src/processing/cleaner.py
```

### 3. Khởi động dashboard

```bash
poetry run streamlit run src/dashboard/app.py
```

Mở trình duyệt tại `http://localhost:8501`

---

## Cấu trúc project

```
src/
  scrapers/        # Web scrapers (6 nguồn)
  processing/      # Làm sạch, dedup, chuẩn hóa lương, extract skill
  analysis/        # Skill ranking, salary stats, location, AI impact
  data/            # Skill taxonomy (305 skills, 13 categories)
  dashboard/       # Streamlit app & pages
data/
  raw/             # Dữ liệu thô JSON (gitignored)
  processed/       # Dữ liệu đã xử lý (gitignored)
  db/              # SQLite database (gitignored)
tests/             # pytest test suite
```

---

## Development

```bash
# Chạy tests
poetry run pytest

# Chạy với coverage
poetry run pytest --cov=src

# Format code
poetry run black .

# Lint
poetry run ruff check .
```

---

## Tiến độ

- [x] Skill taxonomy (305 skills, 13 categories, 635 aliases)
- [x] ITviec scraper
- [x] TopCV scraper
- [ ] VietnamWorks scraper
- [ ] Glints scraper
- [ ] Vieclam24h scraper
- [ ] 123job scraper
- [ ] Data processing pipeline
- [ ] SQLite schema
- [ ] Dashboard (6 trang)

---

## License

MIT
