---
id: "001"
title: "Thiết kế skill taxonomy cho thị trường IT Việt Nam"
status: "completed"
area: "backend"
agent: "@builder"
priority: "high"
created_at: "2026-04-18"
due_date: null
started_at: "2026-04-18"
completed_at: "2026-04-18"
prd_refs: ["FR-014", "FR-020", "FR-021"]
blocks: ["005", "008", "009", "011"]
blocked_by: []
---

## Description

Tạo file `src/data/skills_taxonomy.py` định nghĩa tất cả keyword groups dùng để extract kỹ năng từ JD. Taxonomy phải phù hợp với thị trường IT Việt Nam: bao gồm cả từ tiếng Anh, viết tắt phổ biến, và cách viết thường thấy trong JD Việt Nam.

Cấu trúc: một dict `SKILLS_TAXONOMY` với key là tên category, value là dict mapping canonical skill name → list các keyword/alias.

## Acceptance Criteria

- [ ] File `src/data/skills_taxonomy.py` tồn tại và importable
- [ ] Có tối thiểu 10 categories: Programming Languages, Frameworks & Libraries, Databases, Cloud Platforms, DevOps & Tools, AI/ML & Data Science, AI/GenAI Tools, Mobile, Testing, Soft Skills
- [ ] Có tối thiểu 150 canonical skills với đầy đủ aliases
- [ ] Category AI/GenAI phải bao gồm: ChatGPT, LLM, RAG, Prompt Engineering, Langchain, Hugging Face, Copilot, Gemini, v.v.
- [ ] Có hàm `get_all_keywords() -> dict[str, str]` trả về flat map từ keyword → canonical skill name (dùng cho matching)
- [ ] Có hàm `get_categories() -> list[str]` trả về danh sách categories
- [ ] Viết unit test `tests/test_taxonomy.py` kiểm tra: import ok, no duplicate keywords, get_all_keywords() không rỗng
- [ ] Chạy `poetry run pytest tests/test_taxonomy.py` pass

## Technical Notes

- Tham khảo project andresvourakis/ai-ds-job-market: dùng ~230 keyword groups, có 10 categories
- Keyword matching phải case-insensitive (normalize về lowercase khi build flat map)
- Aliases cần bao gồm viết tắt VN phổ biến: "JS" → JavaScript, "PY" → Python, "K8s" → Kubernetes
- Một keyword không được xuất hiện trong 2 canonical skills khác nhau (sẽ gây ambiguity khi match)
- Không dùng regex phức tạp ở tầng taxonomy — chỉ literal strings; regex xử lý ở skill_extractor.py sau
- File chỉ là pure Python data (không import gì ngoài stdlib nếu cần)

## History

| Date | Agent / Human | Event |
|------|--------------|-------|
| 2026-04-18 | human | Task created |
| 2026-04-18 | orchestrator | Task started, delegated to @builder |
