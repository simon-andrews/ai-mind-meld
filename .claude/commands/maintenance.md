---
description: Routine maintenance pass — prevent bit rot, keep deps and docs current, open a PR
---

Do a routine maintenance pass on this repository. The goal is to prevent bit rot
and keep things current with best practices — NOT to add features or change what
the project does. Stay in scope: prevent rot, don't add scope.

This runs non-interactively in an ephemeral container, so there is no human to
ask mid-run. All feedback happens afterward, by reviewing, commenting on, or
rejecting the PR you open. Do NOT wait for confirmation: make the safe changes
directly, and for anything riskier make your best-justified attempt and explain
it clearly in the PR body so it's easy to reject or amend. Never leave the run
blocked on a question.

First, get your bearings: figure out the languages, package manager(s), and
tooling actually in use here before changing anything. Then work through this
checklist.

1. Dependencies
   - Update dependencies to current stable versions: runtime deps, dev deps, and
     any pinned tool/hook revisions (e.g. pre-commit, CI actions).
   - Where the same tool's version is pinned in more than one place, keep those
     pins in sync with each other.
   - Major-version bumps are in scope, not something to defer. Apply them, fix
     whatever they break, and call them out in the PR body with links to
     changelogs/migration notes so they're easy to review or reject.

2. Language / runtime version
   - Track modern language runtimes as they're released. If a newer stable
     runtime is available and worth adopting, bump it everywhere it's declared
     (version manifests, version-pin files, CI matrices, classifiers, docs) and
     migrate code as needed.
   - Adopting a dependency that requires a newer runtime is fine when justified —
     make the matching runtime bump and explain the tradeoff in the PR body.

3. Verify it still works
   - Run the linter, formatter, build, and any tests. Fix anything the updates
     broke.
   - If the project has no tests, don't write a feature suite — just confirm it
     still builds/imports/runs and note the gap in the PR body.

4. Staleness / drift
   - Find and modernize deprecated API usage, deprecation warnings, and patterns
     that are no longer the recommended way to do things with the current
     versions of the libraries in use.
   - Check that docs (README, AGENTS.md / CLAUDE.md, etc.) still match reality:
     commands, config flags, env vars, supported versions.
   - Check CI config and the tool versions used in workflows for drift, and fix
     it.
   - Fix pinned-but-outdated tool versions, end-of-life runtimes, and references
     to things that no longer exist.

5. Security — FIX these, don't just note them
   - Update vulnerable dependency versions.
   - Remove accidentally committed secrets (and note in the PR that they need
     rotation).
   - Tighten overly broad permissions (CI tokens, workflow permissions, etc.).
   - If a security fix is genuinely too risky to apply blind, apply the safest
     mitigation you can and flag the rest prominently in the PR body.

Rules of engagement:
   - No new features, no opinionated rewrites, no reformatting of unrelated code.
   - Make small, reviewable commits grouped by concern, each with a clear message
     describing what changed and why.
   - Do all work on a dated maintenance branch (e.g. maintenance/YYYY-MM-DD).
   - At the END, open a PR titled "Routine maintenance — YYYY-MM-DD". In the body
     include: what changed, grouped by concern; major upgrades with
     changelog/migration links; security fixes (call out anything needing
     rotation or follow-up); what you deliberately left alone and why; and a
     short list of anything that wants a human's judgment call. The PR is the
     deliverable and the place for all "needs review" notes — there is no
     interactive step.
   - If there's genuinely nothing to do, say so and don't open an empty PR.
