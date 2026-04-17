# VN Tech Job Market Dashboard — Claude Instructions

> Stack: Python 3.11 · Streamlit · Pandas · Plotly · SQLite · Poetry
> Last updated: 2026-04-18

## Project Context

VN Tech Job Market Dashboard phân tích hàng nghìn tin tuyển dụng công nghệ thực tế từ các trang việc làm Việt Nam (ITviec, TopCV, VietnamWorks) để xác định kỹ năng nào được yêu cầu nhiều nhất, mức lương theo vị trí/địa điểm/seniority, và mức độ ảnh hưởng của AI/GenAI đến thị trường lao động IT Việt Nam. Người dùng là lập trình viên, data scientist, và HR tại Việt Nam.

**Tech stack summary**: Streamlit (UI) · Python scripts (scraping + processing) · Pandas/Plotly (analysis) · SQLite (storage) · Poetry (deps)

---

## Agents Available

**Mandatory delegation — this is not optional.** Every task that falls within a specialist's domain MUST be routed to that agent. Do not implement code, design schemas, write docs, or configure pipelines yourself — delegate. Only handle directly: project-level questions, routing decisions, and tasks explicitly outside all specialist domains.

| Agent | Role | Invoke when... |
|-------|------|----------------|
| `planner` | Backlog & architecture | "What's next?", sprint planning, feature decomposition, tech decisions, ADRs, new feature design before implementation |
| `builder` | All application code | Streamlit pages, scraping scripts, data processing, analysis modules — specify domain in request |
| `designer` | UX & content | Dashboard layout specs, chart design, color scheme, data visualization choices |
| `quality` | Testing & documentation | pytest tests, test strategy, coverage gaps, user guide updates |
| `infra` | Infrastructure & pipelines | CI/CD workflows, Docker, deployment config |

---

## Critical Rules

These apply to all agents at all times. No exceptions without explicit human instruction.

1. **PRD.md requires explicit human approval to modify.** Do not edit it unless the human has clearly instructed you to do so in the current conversation. Read it to understand requirements.
2. **TODO.md is the living backlog.** Agents may add items, mark items complete, and move items to "Completed". Preserve section order and existing item priority — do not reorder items within a section unless explicitly asked to reprioritize.
3. **All commits use Conventional Commits format** (see Git Conventions below).
4. **Update the relevant `docs/` file** after every significant change before marking a task complete.
5. **Run tests before marking any implementation task complete.**
6. **Never hardcode secrets, credentials, or environment-specific values** in source code. Use `.env` files.
7. **Consult `docs/technical/DECISIONS.md`** before proposing changes that may conflict with prior architectural decisions.
8. **Always delegate to the right specialist.** If a task touches application code, design/UX, testing/documentation, or infrastructure — invoke the appropriate agent immediately. Do not implement it yourself.
9. **Commit your own changes; never push.** After completing your work, create a local commit (Conventional Commits format). Do not `git push`.
10. **When invoking `builder`, specify the domain** (e.g. "scraper task — add ITviec scraper" or "dashboard task — add salary analysis page").

---

## Slash Commands

| Command | What it does |
|---------|--------------|
| `/orchestrate <task>` | Full multi-agent task execution — decompose, plan, branch, execute in waves |
| `/status` | Render a live project health card (tasks, commits, open PRs, blockers) |
| `/start` | Run project onboarding from `START_HERE.md` |
| `/sync-template` | Pull latest agent definitions and templates from upstream |

---

## MCP Servers

| Server | Purpose | Agents that use it |
|--------|---------|-------------------|
| `sequential-thinking` | Structured multi-step reasoning scratchpad | `planner` |
| `context7` | Live, version-accurate library documentation | `builder`, `infra` |

---

## Project Structure

```
src/
  scrapers/           # Web scrapers for each job board
    itviec.py         # ITviec.com scraper
    topcv.py          # TopCV.vn scraper
    vietnamworks.py   # VietnamWorks.com scraper
    glints.py         # Glints.com/vn scraper
    vieclam24h.py     # Vieclam24h.vn scraper
    job123.py         # 123job.vn scraper
  processing/         # Data cleaning and skill extraction
    cleaner.py        # Raw data normalization
    skill_extractor.py # Keyword-based skill matching
    salary_parser.py  # Salary range normalization (VND)
  analysis/           # Analysis modules
    skills.py         # Skill frequency & ranking
    salary.py         # Salary statistics
    location.py       # Geographic distribution
    ai_impact.py      # AI/GenAI adoption analysis
  data/               # Skill keyword definitions
    skills_taxonomy.py  # Vietnamese tech skills keyword groups
  dashboard/          # Streamlit pages
    app.py            # Main entry point
    pages/            # Multi-page Streamlit pages
      01_skills.py
      02_salary.py
      03_location.py
      04_ai_impact.py
      05_job_explorer.py
      06_companies.py
data/
  raw/                # Raw scraped data (JSON)
  processed/          # Cleaned and normalized data
  db/                 # SQLite database
tests/
  test_scraper.py
  test_processing.py
  test_analysis.py
docs/
  user/USER_GUIDE.md
  technical/
```

---

## Git Conventions

### Commit Format
```
<type>(<scope>): <short description>
```
**Types**: `feat` · `fix` · `docs` · `refactor` · `test` · `chore` · `perf` · `data`

Examples:
```
feat(scraper): add ITviec job listing scraper
feat(dashboard): add salary analysis page
data(skills): expand AI/ML keyword taxonomy for Vietnamese market
fix(parser): handle null salary ranges from TopCV
```

### Branch Naming
```
feature/<ticket-id>-short-description
fix/<ticket-id>-short-description
data/<description>
```

---

## Code Style

- **Language**: Python 3.11+
- **Formatter**: Black (`black .`)
- **Linter**: Ruff (`ruff check .`)
- **Type hints**: Required on all public functions
- **No `print()`** in production code — use Python `logging` module
- **No commented-out code** committed — delete it or track in TODO.md
- **Docstrings**: Google style, only on public functions with non-obvious behavior

---

## Testing Conventions

- **Test runner**: pytest
- **Test location**: `tests/` mirroring `src/` structure
- **Run tests**: `poetry run pytest`
- **Run with coverage**: `poetry run pytest --cov=src`
- **Coverage target**: 70% for new modules
- Mock external HTTP calls with `responses` or `pytest-httpx`
- Never make real HTTP requests in tests — use fixture data from `tests/fixtures/`

---

## Environment & Commands

- **Python**: 3.11+ (see `.python-version`)
- **Package manager**: Poetry
- `poetry install` — install dependencies
- `poetry run streamlit run src/dashboard/app.py` — start dashboard
- `poetry run python src/scrapers/run_all.py` — run all scrapers
- `poetry run pytest` — run tests
- `poetry run black .` — format code
- `poetry run ruff check .` — lint check

---

## Key Documentation

@docs/technical/ARCHITECTURE.md
@docs/technical/DECISIONS.md
@docs/technical/DATABASE.md
@docs/user/USER_GUIDE.md
