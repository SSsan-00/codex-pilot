# Capability boundaries

Read this file only when current Codex capabilities, model identifiers, installation surfaces, Parent detection, Fast, or Ultra affect a decision.

## Current verified design assumptions

The repository's compatibility snapshot is documented in [`docs/compatibility.md`](../../../docs/compatibility.md). Re-check the current host instead of treating that snapshot as a permanent catalog.

### Skills and plugins

- A distributable plugin has `.codex-plugin/plugin.json` and may bundle one or more skills under `skills/`.
- A skill requires `SKILL.md` with `name` and `description`. Codex may invoke it explicitly or implicitly from its description.
- Installed plugin components become available in a new chat or CLI session. Standalone user skills can be installed under the host-documented user skill path; Codex supports symlinked skill folders.
- `AGENTS.md` is loaded by Codex for project-specific guidance. Pilot must not duplicate or replace it.
- Hooks are available but intentionally absent from Codex Pilot: routing is a judgment workflow, and a lifecycle hook would add trust, portability, and failure surface without enabling live Parent switching.

### Worker controls

When the spawn interface accepts `model` and reasoning/effort, set both explicitly. Explicit spawn values normally override agent defaults. When omitted, a child may inherit the Parent; selecting a model without an effort may instead use that model's default. Preserve exact host-reported IDs.

If these controls are absent, do not mutate the user's persistent Codex configuration to emulate them. Use the capable Parent, a host-provided custom agent, or an advisory route.

### Parent detection and switching

A skills-only plugin has no documented portable API that returns the live Parent model and reasoning effort. Disk configuration is insufficient because a turn may override it. Treat Parent values as known only when the host exposes them in runtime metadata or the user states them.

A skill cannot change the already-running Parent mid-turn. It can recommend a new composer/CLI selection for a new turn or session.

### Ultra

Ultra is a supported-model and account-dependent execution mode combining maximum reasoning with proactive subagent delegation. It is not an exact model ID. Pilot may use an already active Ultra environment or recommend it, but cannot claim to enable it through `SKILL.md`, `openai.yaml`, or `plugin.json`.

Official surfaces can differ in how they enumerate `max` and `ultra`. Trust the current host's advertised values and fall back without failure.

### Fast

Fast is controlled by the Codex host, such as the interactive CLI command `/fast` or host configuration on supported models. There is no documented Skill or Plugin manifest field that toggles Fast for the live turn. `allow_fast` therefore grants policy permission only. Require observable status before stating that Fast is active.

### Platform behavior

Keep the skill instructions shell-neutral. Respect the current environment's path syntax; never translate Windows paths to WSL paths implicitly.

- macOS and Linux: use tools already provided by the host and project.
- Windows Native: prefer PowerShell or cross-platform project commands; do not assume `rm`, `grep`, `sed`, or `awk`.
- WSL: treat Linux paths and mounted Windows paths as presented.

Codex Pilot has no mandatory runtime script, shell, external router, SaaS, API key, or MCP dependency. Actual project commands may still depend on the project being worked on.

## Privacy

Do not persist prompt or source contents for routing. If the host or user requests metadata, limit it to classification, selected logical family and exact advertised ID, effort, escalation count, reason category, and timestamp. Never record secrets, credentials, source text, prompt text, or environment-variable values.
