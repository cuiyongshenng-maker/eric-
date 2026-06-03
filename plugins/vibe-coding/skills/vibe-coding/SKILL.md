---
name: vibe-coding
description: Use when the user wants to build, prototype, modify, or debug software by describing the desired result in natural language and iterating with Codex. This skill is especially useful for MVPs, small apps, scripts, websites, plugins, and product ideas where the user may not know the exact implementation details.
---

# Vibe Coding

Use this workflow to convert a rough idea into a working, verified software change.

## Operating Mode

- Prefer action over long planning when the request is concrete enough to start.
- Keep the first version small, usable, and easy to change.
- Preserve the existing project style, framework, and directory structure.
- Treat unclear requirements as product assumptions and state them briefly before implementing.
- Ask the user only when a missing decision changes the product, security model, data ownership, or deployment target.
- Do not implement surveillance, credential theft, bypasses, or hidden data collection. Offer consent-based alternatives.

## Workflow

1. Inspect the current project before editing.
2. Identify the smallest useful version of the requested feature.
3. Make scoped changes with clear filenames and minimal new dependencies.
4. Run the most relevant checks available locally.
5. Fix issues found during verification.
6. Report what changed, how it was verified, and what remains.

## Product Defaults

- For apps, build the actual working screen first instead of a marketing landing page.
- For prototypes, favor simple local storage or mock data unless the user asked for a real backend.
- For user-facing UI, include practical controls, empty states, loading states, and error states when relevant.
- For scripts, provide direct commands and sensible defaults.
- For GitHub handoff, include a concise README only when the project does not already explain how to run the code.

## Verification

Use the strongest cheap check available:

- Run existing tests for backend or library changes.
- Run linters or type checks when configured.
- Start the dev server and inspect the app for frontend changes.
- For one-file scripts, run the script with a representative input.

If verification cannot run because of missing dependencies, network limits, credentials, or platform restrictions, say exactly what blocked it.

## Final Response

Keep the close-out short:

- Name the changed files.
- State the verification performed.
- Mention any known limitation or next concrete step.
