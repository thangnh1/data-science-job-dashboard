# VN Tech Job Market Dashboard

Phân tích thị trường việc làm IT Việt Nam dựa trên dữ liệu thực tế từ ITviec, TopCV, VietnamWorks, Glints, Vieclam24h và 123job.

---

## Cài đặt

### Yêu cầu

- Python 3.11+
- Poetry

### Các bước

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

## Chạy ứng dụng

```bash
# Thu thập dữ liệu
poetry run python src/scrapers/run_all.py

# Khởi động dashboard
poetry run streamlit run src/dashboard/app.py
```

Mở trình duyệt tại `http://localhost:8501`
