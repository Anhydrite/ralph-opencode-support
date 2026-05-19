# AGENTS.md

Ralph is an autonomous AI agent loop that runs AI coding tools ([Amp](https://ampcode.com), [Claude Code](https://docs.anthropic.com/en/docs/claude-code), or [OpenCode](https://github.com/anomalyco/opencode)) repeatedly until all PRD items are complete. Based on [Geoffrey Huntley's Ralph pattern](https://ghuntley.com/ralph/).

## Commands

```bash
# Run Ralph with Amp (default)
./ralph.sh [max_iterations]

# Run Ralph with Claude Code
./ralph.sh --tool claude [max_iterations]

# Run Ralph with OpenCode
./ralph.sh --tool opencode [max_iterations]

# Flowchart dev server
npm run dev      # from ./flowchart/

# Flowchart build (typecheck + vite build)
npm run build    # from ./flowchart/

# Inspect task progress
jq '.userStories[] | {id, title, passes}' prd.json
```

## Key Files

| File | Purpose |
|------|---------|
| `ralph.sh` | Bash loop spawning fresh AI instances per iteration |
| `prompt.md` | Prompt template for **Amp** instances |
| `CLAUDE.md` | Prompt template for **Claude Code** instances |
| `OPENCODE.md` | Prompt template for **OpenCode** instances |
| `prd.json` (gitignored) | User stories with `passes` boolean — the task list |
| `prd.json.example` | Reference format for prd.json |
| `progress.txt` (gitignored) | Append-only learnings across iterations |
| `skills/prd/` | Skill for generating PRDs |
| `skills/ralph/` | Skill for converting PRDs to prd.json |
| `flowchart/` | React Flow + Vite + TypeScript interactive visualization |
| `.claude-plugin/` | Claude Code marketplace plugin manifest |
| `.github/workflows/deploy.yml` | Deploys `flowchart/` to GitHub Pages on push to `main` |

## Architecture

- **Each iteration = fresh context.** No memory between iterations except git history, `progress.txt`, and `prd.json`.
- **Branch naming:** Features use `ralph/<feature-name>` (kebab-case).
- **Stop condition:** Spawning loop exits when an iteration outputs `<promise>COMPLETE</promise>` (all stories `passes: true`).
- **Archive:** When `branchName` changes, `ralph.sh` automatically copies `prd.json` and `progress.txt` to `archive/YYYY-MM-DD-feature-name/` and resets progress.
- **Autonomous flags:** Amp runs with `--dangerously-allow-all`; Claude Code with `--dangerously-skip-permissions --print`; OpenCode with `--dangerously-skip-permissions`.
- **Dependency:** `jq` must be installed for the `ralph.sh` script.

## Story Rules

- Stories execute in **priority order** (lowest number first). Earlier stories must not depend on later ones.
- Typical order: schema → backend → UI → aggregates.
- Every story must be completable in one context window. If you can't describe it in 2-3 sentences, split it.
- Each story must include `"Typecheck passes"` in `acceptanceCriteria`. UI stories should also include `"Verify in browser using dev-browser skill"`.

## Flowchart Visualization

The `flowchart/` directory is a standalone React + Vite + TypeScript app using `@xyflow/react`. Built by `tsc -b && vite build`. Base path is `/ralph/` for GitHub Pages deployment.

## CI / Publishing

- **Only CI:** GitHub Actions deploys `flowchart/dist` to GitHub Pages on push to `main`.
- **No test suite** exists in this repo. Quality verification relies on typecheck (`tsc -b`) and the interactive flowchart.

## Gotchas

- The `.gitignore` excludes `prd.json`, `progress.txt`, and `.last-branch` — these are runtime state, not checked in.
- `prompt.md` is for Amp; `CLAUDE.md` is for Claude Code; `OPENCODE.md` is for OpenCode. They are **not interchangeable**.
- Edited AGENTS.md files are committed alongside story changes for future iterations.
