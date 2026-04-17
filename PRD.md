# Product Requirements Document

> [!WARNING]
> **HUMAN APPROVAL REQUIRED TO EDIT**
> This document is the source of truth for what we are building.
> Claude agents must READ this document to understand requirements.
> **Do not edit, rewrite, or "update to reflect current state" unless the human has explicitly instructed you to do so in the current conversation.**
> When in doubt, leave it unchanged and ask the human.

---

**Version**: 1.0
**Status**: Draft
**Last updated by human**: 2026-04-18
**Product owner**: propero.test@gmail.com

---

## 1. Executive Summary

VN Tech Job Market Dashboard là một ứng dụng Streamlit phân tích thị trường việc làm công nghệ Việt Nam bằng cách thu thập và xử lý tin tuyển dụng thực tế từ ITviec, TopCV, và VietnamWorks. Nó giải quyết vấn đề thiếu dữ liệu minh bạch về kỹ năng được yêu cầu, mức lương thực tế, và xu hướng AI/GenAI trong ngành IT Việt Nam. Người dùng chính là lập trình viên và data scientist muốn định hướng nghề nghiệp, HR/recruiter cần benchmark thị trường. Sau khi sử dụng, người dùng có thể đưa ra quyết định học kỹ năng mới, thương lượng lương, hoặc tuyển dụng dựa trên dữ liệu thực tế của thị trường Việt Nam.

---

## 2. Problem Statement

### 2.1 Current Situation

Hiện tại, người tìm việc IT tại Việt Nam phải tự tổng hợp thông tin bằng cách duyệt thủ công các trang ITviec, TopCV, VietnamWorks — tốn vài giờ mỗi lần. HR và recruiter dựa vào cảm tính hoặc khảo sát lương định kỳ (thường lỗi thời 6-12 tháng) để benchmark. Không có nguồn nào cung cấp dữ liệu tổng hợp, cập nhật, và trực quan về thị trường IT Việt Nam.

### 2.2 The Problem

Thiếu công cụ phân tích thị trường việc làm IT Việt Nam dựa trên dữ liệu thực tế: kỹ năng nào đang được demand cao nhất, mức lương theo role/seniority/địa điểm là bao nhiêu, các công ty nào đang tuyển dụng nhiều nhất, và AI/GenAI đã thâm nhập vào JD Việt Nam đến mức nào.

### 2.3 Why Now

Thị trường IT Việt Nam đang bùng nổ (2024-2026): số lượng tin tuyển dụng tăng mạnh, AI/GenAI xuất hiện trong ngày càng nhiều JD, nhưng chưa có công cụ nào tổng hợp và phân tích dữ liệu này một cách có hệ thống cho thị trường Việt Nam.

---

## 3. Goals & Success Metrics

### 3.1 Business Goals

- Cung cấp dashboard phân tích thị trường IT Việt Nam dựa trên dữ liệu thực tế, cập nhật định kỳ
- Trở thành nguồn tham chiếu tin cậy cho cộng đồng developer/data scientist Việt Nam
- Demonstrating open data analysis methodology có thể reproduce và mở rộng

### 3.2 Success Metrics

| Metric | Baseline | Target | How Measured |
|--------|----------|--------|--------------|
| Số tin tuyển dụng trong database | 0 | ≥ 2.000 tin | SQLite row count |
| Số nguồn dữ liệu tích hợp | 0 | ≥ 6 nguồn (ITviec, TopCV, VietnamWorks, Glints, Vieclam24h, 123job) | Scraper modules |
| Số trang dashboard hoạt động | 0 | 6 trang | Streamlit pages |
| Độ chính xác phân loại kỹ năng | N/A | ≥ 85% | Manual spot-check 100 JDs |
| Thời gian chạy toàn bộ pipeline | N/A | < 30 phút | Script runtime |

---

## 4. User Personas

### Persona: Minh — Developer tìm việc

- **Role**: Backend developer 3 năm kinh nghiệm, đang cân nhắc chuyển việc
- **Goals**: Biết kỹ năng nào đang hot, mức lương thị trường cho level của mình, công ty nào đang tuyển
- **Pain points**: Phải duyệt thủ công hàng chục trang web, lương posting thường là khoảng rộng hoặc "thỏa thuận"
- **Technical level**: Developer — thoải mái dùng tool kỹ thuật
- **Usage frequency**: Mỗi 2-3 tháng khi cân nhắc thay đổi công việc

### Persona: Linh — HR / Talent Acquisition

- **Role**: HR Manager tại công ty công nghệ tầm trung, phụ trách tuyển dụng IT
- **Goals**: Benchmark lương thị trường, biết đối thủ đang tuyển gì, tối ưu JD để thu hút ứng viên
- **Pain points**: Báo cáo lương thị trường đắt, lỗi thời; không có dữ liệu cho mảng IT cụ thể tại Việt Nam
- **Technical level**: Non-technical — chỉ dùng giao diện web, không đọc code
- **Usage frequency**: Hàng tuần khi có nhu cầu tuyển dụng

### Persona: An — Data Scientist / Career Switcher

- **Role**: Kỹ sư phần mềm 5 năm, đang học Data Science và muốn chuyển hướng
- **Goals**: Hiểu thị trường DS/ML/AI Việt Nam yêu cầu gì, mức lương entry-level DS so với senior SE, AI/GenAI đang ảnh hưởng thế nào
- **Pain points**: Thông tin về DS job market Việt Nam rất ít, phần lớn resource là của thị trường US/global
- **Technical level**: Developer — hiểu data, biết Python
- **Usage frequency**: Hàng tuần trong giai đoạn học và tìm việc

---

## 5. Functional Requirements

> Requirements are numbered FR-XXX for unambiguous cross-referencing by agents and in tests.

### 5.1 Data Collection (Scrapers)

- **FR-001**: Hệ thống phải thu thập tin tuyển dụng từ ITviec.com bao gồm: tiêu đề, công ty, địa điểm, mức lương (nếu có), mô tả công việc, ngày đăng, loại hình (toàn thời gian/bán thời gian/remote)
- **FR-002**: Hệ thống phải thu thập tin tuyển dụng từ TopCV.vn với cùng cấu trúc dữ liệu như FR-001
- **FR-003**: Hệ thống phải thu thập tin tuyển dụng từ VietnamWorks.com với cùng cấu trúc dữ liệu như FR-001
- **FR-006**: Hệ thống phải thu thập tin tuyển dụng từ Glints.com/vn với cùng cấu trúc dữ liệu như FR-001 (tech-focused, startup & công ty nước ngoài)
- **FR-007**: Hệ thống phải thu thập tin tuyển dụng từ Vieclam24h.vn với cùng cấu trúc dữ liệu như FR-001 (cover IT entry-level)
- **FR-008**: Hệ thống phải thu thập tin tuyển dụng từ 123job.vn với cùng cấu trúc dữ liệu như FR-001 (SME & mid-market)
- **FR-004**: Scraper phải xử lý được phân trang và thu thập tối thiểu 500 tin mỗi nguồn mỗi lần chạy
- **FR-005**: Dữ liệu thô phải được lưu vào file JSON với timestamp, trước khi xử lý

### 5.2 Data Processing

- **FR-010**: Hệ thống phải deduplicate tin tuyển dụng giống nhau xuất hiện trên nhiều nguồn (dựa trên tiêu đề + công ty + ngày đăng)
- **FR-011**: Hệ thống phải chuẩn hóa địa điểm về: Hà Nội, TP.HCM, Đà Nẵng, Khác, Remote
- **FR-012**: Hệ thống phải parse và chuẩn hóa mức lương về dạng số (VND/tháng), xử lý các format: "15-25 triệu", "$1000-1500", "Thỏa thuận"
- **FR-013**: Hệ thống phải phân loại seniority từ tiêu đề JD: Junior (0-2 năm), Middle (2-5 năm), Senior (5+ năm), Lead/Manager
- **FR-014**: Hệ thống phải extract kỹ năng từ mô tả công việc bằng keyword matching với taxonomy đã định nghĩa

### 5.3 Skill Analysis Dashboard

- **FR-020**: Dashboard phải hiển thị top 20 kỹ năng được yêu cầu nhiều nhất, có thể filter theo: category (Programming, Database, Cloud, ML/AI, etc.), địa điểm, seniority
- **FR-021**: Dashboard phải hiển thị kỹ năng theo category: Programming Languages, Frameworks, Databases, Cloud, DevOps, AI/ML, Soft Skills
- **FR-022**: Charts phải là interactive (Plotly) — hover để xem số liệu, click để filter

### 5.4 Salary Analysis Dashboard

- **FR-030**: Dashboard phải hiển thị phân phối lương (histogram + box plot) theo: role type, seniority level, địa điểm
- **FR-031**: Dashboard phải hiển thị salary premium cho từng kỹ năng (kỹ năng nào đi kèm mức lương cao hơn)
- **FR-032**: Dashboard phải so sánh lương giữa các nguồn (ITviec vs TopCV vs VietnamWorks)
- **FR-033**: Chỉ hiển thị lương khi có tối thiểu 10 data points để đảm bảo độ tin cậy thống kê

### 5.5 Location Analysis Dashboard

- **FR-040**: Dashboard phải hiển thị phân phối tin tuyển dụng theo địa điểm (Hà Nội, TP.HCM, Đà Nẵng, Khác, Remote)
- **FR-041**: Dashboard phải hiển thị kỹ năng được yêu cầu nhiều nhất theo từng thành phố
- **FR-042**: Dashboard phải hiển thị so sánh mức lương giữa các thành phố cho cùng một role

### 5.6 AI/GenAI Impact Analysis Dashboard

- **FR-050**: Dashboard phải hiển thị tỷ lệ % tin tuyển dụng đề cập đến AI/GenAI keywords (ChatGPT, LLM, RAG, Prompt Engineering, v.v.)
- **FR-051**: Dashboard phải hiển thị trend theo thời gian: AI/GenAI keywords xuất hiện nhiều hơn theo tháng
- **FR-052**: Dashboard phải phân tích theo seniority: level nào được yêu cầu AI skills nhiều nhất
- **FR-053**: Dashboard phải hiển thị salary premium cho vị trí có AI/GenAI requirements so với không có

### 5.7 Job Explorer

- **FR-060**: Người dùng phải có thể search tin tuyển dụng theo từ khóa tự do
- **FR-061**: Người dùng phải có thể filter theo: nguồn, địa điểm, seniority, kỹ năng cụ thể, loại hình (remote/hybrid/onsite)
- **FR-062**: Kết quả phải hiển thị các kỹ năng được highlight trong mô tả công việc
- **FR-063**: Người dùng phải có thể xem full JD và click link sang trang gốc

### 5.8 Company Rankings

- **FR-070**: Dashboard phải hiển thị top 20 công ty tuyển dụng nhiều nhất
- **FR-071**: Dashboard phải hiển thị kỹ năng mà từng công ty yêu cầu phổ biến nhất
- **FR-072**: Dashboard phải hiển thị mức lương trung bình theo công ty (khi có đủ data)

---

## 6. Non-Functional Requirements

### Performance
- Toàn bộ data pipeline (scraping + processing) chạy xong trong < 30 phút
- Dashboard load trang đầu tiên < 3 giây (với data đã cached)
- Streamlit dùng `@st.cache_data` để cache kết quả analysis, TTL 1 giờ

### Data Quality
- Deduplication rate ≥ 95% (không có tin trùng lặp rõ ràng)
- Skill extraction accuracy ≥ 85% trên manual spot-check
- Salary normalization coverage ≥ 60% (40% còn lại là "Thỏa thuận" — chấp nhận được)

### Reliability
- Scraper phải có retry logic (tối đa 3 lần) khi gặp lỗi network
- Scraper phải gracefully skip tin bị lỗi mà không crash toàn bộ pipeline
- Data từ lần chạy trước phải được giữ lại nếu lần chạy mới thất bại

### Accessibility
- Dashboard sử dụng color-blind friendly palette (Plotly qualitative palette)
- Text đủ contrast ratio WCAG AA

### Platform
- Chạy được trên: macOS, Linux, Windows
- Python 3.11+, không yêu cầu database server (SQLite)
- Streamlit phiên bản ≥ 1.30

---

## 7. Out of Scope (v1.0)

- **Real-time data**: v1 chạy scraper thủ công theo lịch, không có live data stream
- **Authentication / user accounts**: Tool dùng locally hoặc deploy public — không cần login
- **Salary prediction model (ML)**: v1 chỉ thống kê mô tả, không dự đoán
- **Mobile app**: Chỉ web dashboard
- **Notifications / alerts**: Không gửi email/Slack khi có tin mới
- **API endpoints**: v1 không expose REST API
- **Automated scheduling / cron**: v1 chạy thủ công, không tự động
- **LinkedIn scraping**: Out of scope — anti-scraping cực mạnh, ToS nghiêm
- **Glassdoor, JobHopin, Ybox**: Để lại cho v2

---

## 8. Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | ITviec và TopCV có chặn scraper không? Cần dùng Playwright/rotating proxy không? | propero.test@gmail.com | Open |
| 2 | Có nên deploy Streamlit app lên Streamlit Cloud để share publicly không? | propero.test@gmail.com | Open |
| 3 | Cần include tên công ty (FPT, VNG, Momo, etc.) vào taxonomy kỹ năng không? | propero.test@gmail.com | Open |

---

## 9. Revision History

| Date | Author | Change Description |
|------|--------|--------------------|
| 2026-04-18 | propero.test@gmail.com | Initial draft |
