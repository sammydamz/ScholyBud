# ScholyBud - School Management System

**Project:** Multi-tenant school management SaaS built with FastAPI + React 19

## Tech Stack

**Backend:** FastAPI, SQLModel, PostgreSQL, JWT, passlib
**Frontend:** React 19, TypeScript, TailwindCSS (Tailwick template), Zustand, React Query
**Offline:** PWA (Service Workers, IndexedDB via Dexie.js)

## Development Workflow

**REQUIRED SKILL:** Always use `react-fastapi-SWE` workflow skill for all development tasks.

### Workflow Steps

1. **Choose Task** - Select task sheet and specific task to work on
2. **Delegate** - Activate `/subagent-driven-development` to assign task to subagent
3. **Frontend Guidelines** - Use `/vercel-react-best-practices` and `/mastering-typescript`
4. **Backend Guidelines** - Use `/fastapi` for all backend code
5. **Spec Check** - Use subagent to verify all specs implemented, fix missing specs
6. **Code Review** - Call `/requesting-code-review` to review completed task (findings only, don't fix)
7. **Review Findings** - Call `/receiving-code-review` to evaluate findings and proceed with fixes
8. **Debug** - Use `/systematic-debugging` when told to fix errors
9. **Commit** - Provide commit title/description (user commits manually, never auto-commit)
10. **Next Task** - Proceed only after user confirms commit and gives approval

### Branch Naming (Required)

```
feature/<description>  # New functionality
fix/<description>      # Bug fixes
chore/<description>    # Setup, config, refactoring
```

**Never push directly to main or dev.**

### Commit Message Format

```
<Imperative Verb> <Specific Description>

✅ Add Student model with attendance tracking
✅ Fix offline sync queue retry mechanism
✅ Configure PWA manifest and service worker

❌ working on stuff
❌ updated files
❌ fix bug
```

- Start with imperative verb: Add, Fix, Update, Remove, Refactor, Configure
- Keep under 72 characters
- Be specific about what changed

## Claude Constraints

**PROHIBITED:**
- Never run `git commit` commands
- Never run `git reset --hard` or destructive git commands
- Never remove or delete commits
- Never write code unless explicitly tasked
- Never proceed to next task without user approval

**REQUIRED:**
- Always use `react-fastapi-SWE` skill for development workflow
- Follow the workflow steps in order
- Provide commit title/description for user to execute
- Wait for user confirmation before proceeding

## Project Structure

```
backend/                 # FastAPI backend
├── api/                 # API routers
├── models/              # SQLModel tables
├── schemas/             # Pydantic schemas
├── core/                # Security, database
└── services/            # Business logic

src/                     # React frontend
├── app/                 # Pages (React Router)
├── components/          # React components
├── lib/                 # API client, hooks, stores
├── services/            # Offline sync, PDF generation
└── types/               # TypeScript definitions
```

## Key Principles

- **Type Safety:** Use TypeScript (frontend) and SQLModel/Pydantic (backend)
- **Offline First:** All features must work offline with Dexie.js + Service Workers
- **Multi-Tenant:** Subdomain-based school isolation
- **Modular:** Schools can enable/disable features
- **TDD:** Write tests before implementation where applicable
- **DRY:** Don't repeat code, extract reusable components
- **YAGNI:** Don't build features not in requirements

## Testing

- Backend: pytest with async support
- Frontend: Vitest (when configured)
- Always run tests before completing a task

## Deployment

- Self-hosted Supabase PostgreSQL
- Docker containers for backend
- Vercel/Netlify for frontend (or self-hosted)

## Commands

**Backend:**
```bash
cd backend && fastapi dev    # Development server
cd backend && fastapi run    # Production server
cd backend && pytest         # Run tests
```

**Frontend:**
```bash
pnpm dev                    # Development server
pnpm build                  # Production build
pnpm lint                   # Lint code
```
