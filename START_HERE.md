# START HERE — Project Template Setup

> **This is a template, not a real project.**
> All placeholder values (wrapped in `[square brackets]`) must be replaced with real project information before development begins.

---

## For Claude: Onboarding Protocol

When the user says **"START!"**, execute this onboarding sequence. Do not wait for further instructions — begin immediately.

### Phase 1: Gather Project Information

Ask the user the following questions. You may ask them in groups of 3–4 at a time to keep the conversation flowing. Do not dump all questions at once.

**Group 1 — Project basics:**
1. What is the name of this project?
2. What does it do in one sentence?
3. Who are the primary users? (e.g., "small business owners", "internal team", "developers")
4. What problem does it solve — what are users doing today without it?

**Group 2 — Tech stack:**
5. What is the frontend technology? (e.g., Next.js, React + Vite, Vue)
6. What is the backend? (e.g., Next.js API routes, Express, FastAPI, Django)
7. What database? (e.g., PostgreSQL, MySQL, SQLite, MongoDB)
8. What ORM or query layer? (e.g., Prisma, Drizzle, SQLAlchemy, raw SQL)
9. What is the hosting/deployment target? (e.g., Railway, Vercel, Fly.io, AWS)
10. What package manager? (npm / pnpm / yarn)
11. What Node version, if applicable?

**Group 3 — Conventions:**
12. What formatter and linter are you using? (e.g., Prettier + ESLint, Biome)
13. What test runner for unit tests? (e.g., Vitest, Jest)
14. What are the dev/build/test commands? (e.g., `npm run dev`, `npm test`)

**Group 4 — Product requirements:**
15. What are the main features this product must have in v1? List them — we'll turn these into FR-XXX requirements.
16. Are there any explicit non-functional requirements? (performance targets, accessibility level, browser support)
17. What is explicitly out of scope for v1?
18. Who is the product owner / decision maker?

**Group 5 — Goals:**
19. What does success look like? Any specific metrics? (e.g., "100 users in first month", "onboarding under 5 minutes")
20. Are there any open decisions you haven't made yet? (e.g., auth provider, payment processor)

---

### Phase 2: Fill in the Documentation

Using the answers, update the following files in order. Replace every `[placeholder]` with real content. Do not leave any placeholder unfilled — if the user doesn't know an answer yet, use a clearly marked `[TBD]` instead.

**Files to update:**

1. **`CLAUDE.md`** — Project name, context paragraph, tech stack summary, code style (formatter, linter, import style), testing conventions (runner, file pattern, commands), environment commands.

2. **`README.template.md`** — Project name, overview paragraphs, tech stack table, Getting Started (prerequisites, install steps, run commands), environment variables table. When complete, rename it to `README.md`, replacing this template's README.

3. **`PRD.md`** — Executive summary, problem statement, user personas (one per user type the user described), functional requirements (convert the feature list into numbered FR-XXX items), non-functional requirements, out of scope list, open questions.

4. **`docs/technical/ARCHITECTURE.md`** — Tech stack table, initial component descriptions, infrastructure environments table. Leave design system and detailed sections as templates — they'll be filled in as the project progresses.

5. **`docs/technical/DECISIONS.md`** — Fill in ADR-001 with the initial tech stack decision: why this stack was chosen over alternatives.

6. **`TODO.md`** — Replace the placeholder items with the actual first tasks derived from the feature list in the PRD. Tag each item with the appropriate `[area:]` label.

---

### Phase 3: Review with the User

After updating all files, summarize what was filled in:
- List each file and the key information added
- Highlight any `[TBD]` items that still need decisions
- Ask: "Does everything look correct? Any changes before we start building?"

Make any corrections the user requests.

---

### Phase 4: Delete This File

Once the user confirms they are satisfied with the documentation:

1. Delete this file (`START_HERE.md`)
2. Confirm deletion with a message: "Setup complete. START_HERE.md has been removed. The project is ready — use TODO.md to see what to work on first."

Do not delete this file before the user explicitly confirms they are happy with the documentation.

---

## Checklist (for reference)

- [ ] All `[placeholders]` in CLAUDE.md replaced or marked `[TBD]`
- [ ] All `[placeholders]` in README.template.md replaced or marked `[TBD]`, then renamed to `README.md`
- [ ] PRD.md has real executive summary, personas, and FR-XXX requirements
- [ ] ARCHITECTURE.md has real tech stack table
- [ ] DECISIONS.md has ADR-001 filled in with real tech stack rationale
- [ ] TODO.md has real first tasks (not template placeholders)
- [ ] User has confirmed satisfaction
- [ ] This file has been deleted
