# Copilot onboarding for this VS Code workspace

This file tells GitHub Copilot/Chat how to work in this repository. Keep it in the repo root so assistants can read it for context.

## Project snapshot

- Name: cmps-357-library-management
- Branch (current): copilot/ensure-fields-are-documented
- Languages & assets: Markdown, CSV, Python scripts, Mermaid diagrams
- Key paths:
  - Docs: `docs/`
  - System: `library-system/` with `data/`, `forms/`, `rules/`, `scripts/`, `tests/`, `workflow/`
  - Transcript: `CHAT_TRANSCRIPT.md`
  - Versioning: `docs/CHANGELOG.md`, `VERSION.md`

## Style and response preferences

- Default tone: friendly, concise, skimmable. Prefer bullets and short paragraphs.
- Prefer concrete edits over high-level advice. If you can make a change, do it.
- VS Code + PowerShell:
  - Assume Windows PowerShell 5.1; chain commands with `;` when needed.
- When proposing terminal commands, keep one per line and mark as optional if not executed.
- Only include generated SVGs if explicitly requested; prefer Mermaid sources (`.mmd`).

## Repository conventions

- Versioning
  - Semantic Versioning.
  - `VERSION.md` is a single source of truth for the current version (e.g., `0.2.0`).
  - `docs/CHANGELOG.md` follows Keep a Changelog; include Added/Changed/Removed and correct dates.
- Documentation updates
  - When adding files, update related READMEs (root and area-specific) and the changelog.
  - Workflows: keep `.mmd` sources in `library-system/workflow/`. Do not reference non-existent SVGs.
  - Tests: `library-system/tests/README.md` documents CSV fixtures; spreadsheets are optional.
- Python code style
  - Always place all imports at the very top of each Python file, never inside functions or classes.
  - If you find imports elsewhere, move them to the top unless there is a documented reason (e.g., conditional/optional imports).
  - All Python code must pass basic type checking (variable types and function return types) using tools like mypy or Pyright.
  - Fix any type mismatches, missing annotations, or incorrect return types before submitting code or documentation updates.
- Transcript logging
  - Append significant actions/findings to `CHAT_TRANSCRIPT.md` with: title/date, branch, request, plan, actions, files changed, notes, quality gates.
- Quality gates
  - For docs-only changes, report Build/Lint/Tests as PASS (n/a to code). For code, run and summarize results.

## How to help in this repo (assistant guidance)

- Before editing
  - Skim `README.md`, `docs/CHANGELOG.md`, and area-specific READMEs for context.
  - If changing workflows or data, also check `library-system/workflow/README.md` and `library-system/data/data_models.md`.
- While editing
  - Make the smallest set of changes needed; don’t reformat unrelated sections.
  - Keep public behavior and file paths stable unless a change is explicitly requested.
- After editing
  - Update `docs/CHANGELOG.md` and `VERSION.md` if the change affects release notes or version.
  - Append a brief entry to `CHAT_TRANSCRIPT.md` using the template at the top of that file.

## Mermaid workflows

- Source files live in `library-system/workflow/`: `reserve_room.mmd`, `check-out-item.mmd`.
- Provide instructions to preview with the VS Code Mermaid extension or `mmdc` CLI; prefer not to commit generated images unless asked.

## Tests

- Python tests are planned (pytest). Suggest minimal fixtures and example tests when adding code.
- Favor CSV fixtures stored under `library-system/tests/` or `library-system/data/` as appropriate.

## Commit and PR notes

- Use descriptive commit messages (summary in 50–72 chars; details after a blank line).
- In PRs, reference the changelog entry, affected docs, and any linked issues.

## Do/Don’t

- Do: keep docs consistent with actual files; prefer source-of-truth updates (CHANGELOG, VERSION, READMEs).
- Do: correct stale references (e.g., remove mentions of missing SVGs).
- Don’t: invent file paths or APIs; verify with a quick scan first.
- Don’t: add heavy dependencies for simple tasks.

## Quickstart (for humans in VS Code)

- View workflows: open `.mmd` files with a Mermaid preview extension.
- Explore data: CSVs live in `library-system/data/`.
- Run scripts: Python scripts in `library-system/scripts/` (configure an environment if needed).
- Track session work: add entries to `CHAT_TRANSCRIPT.md` using the template included there.

