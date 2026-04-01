# photo-poem-generator

Python + Streamlit app using the Anthropic SDK, Pillow, Supabase, and gTTS.

## Development Protocols

- **Plan before editing.** For any change touching more than one file, state the plan and wait for approval before writing code.
- **Surgical edits only.** Edit the specific lines that need changing. Never rewrite an entire file to make a small fix.
- **Run tests after fixes.** After any bug fix, run `python -m pytest` (if tests exist) automatically without asking.
- **Python conventions.** Use `uv` for package management. Do not add dependencies beyond what's in `requirements.txt` without asking. Always prefix project tools (`ruff`, `mypy`, `pytest`) with `uv run` to ensure the correct virtual environment is used.
- **Compact after features.** Run `/compact` after each feature is complete to keep context lean.

## Git Workflow

- All commits must pass pre-commit hooks. If a commit fails, analyze the hook output, fix the errors, and re-attempt the commit.
- **Atomic commits.** Each commit must represent one logical change. Never bundle a feature and a bug fix in the same commit.
- **Conventional commits.** Use the format `type(scope): description` where type is one of: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`. Example: `feat(prompts): per-style poet selection`.
- **Stage selectively.** Use `git add <file>` — never `git add -A` or `git add .` — to keep unrelated changes out of a commit.

## Interaction Standards

- **Demand clarity on vague requests.** If a request lacks a specific file, behaviour, or success criterion, ask 2–3 targeted questions before implementing anything.

## Safety & FinOps

- **No new packages without a name check.** Before any `uv add`, confirm the package name is the canonical one (e.g. `pillow` not `Pillow`, `python-dotenv` not `dotenv`). Typosquatting is real. If unsure, check PyPI directly.
- **Loop prevention.** If the same error recurs after 3 distinct fix attempts, stop and ask the user for a Mental Reset rather than continuing to iterate blindly.

## Critical Thinking & Verification Protocol

- **Verify before proposing.** Read or grep the actual file before suggesting changes. Never assume file structure or content.
- **Mandatory pushback.** If a request is insecure, suboptimal, or inconsistent with project patterns, say so and propose a better alternative before complying.
- **Risk section required.** Every multi-step plan must include a "Risks / Failure Modes" section before execution begins.
- **No assumed paths.** Do not reference a file, library, or import that hasn't been confirmed to exist via a tool call.
- **Edge-case callout.** When implementing logic that handles external data (API responses, user uploads, database results), explicitly identify the most likely failure point before writing code — null/empty responses, wrong types, network errors.
- **Code review agent for complex changes.** For changes involving new data flows, API integrations, or logic with multiple branches, suggest spawning a code-review subagent before the user approves a PR.
