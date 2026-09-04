# Configuration and Ponytail integration

Read this file when resolving Pilot settings, applying a user override, or deciding whether to use Ponytail.

## Precedence

Resolve each setting independently in this order:

1. explicit instruction in the current user request;
2. project file `<repo-root>/.codex-pilot.toml`, when present and readable;
3. user file `$CODEX_HOME/codex-pilot.toml`, when present and readable (`$CODEX_HOME` normally defaults to the user's `.codex` directory);
4. the defaults below.

Do not confuse these optional Pilot files with Codex's official `config.toml`. Never create or edit either Pilot file unless the user asks. Do not search broadly for them, and do not fail when sandbox policy prevents reading a user-level file.

## Defaults

```toml
policy = "quality"

allow_fast = false
allow_ultra = true

min_reasoning = "medium"
max_reasoning = "max"

max_escalations = 2
max_agents = 3

ponytail = "auto"

show_routing = true

suggest_parent_upgrade = true
suggest_parent_downgrade = true
```

Supported values:

- `policy`: `quality`, `balanced`, or `throughput`.
- `min_reasoning` and `max_reasoning`: logical ordered levels `low`, `medium`, `high`, `xhigh`, and `max`. Accept `ultra` only as a host-advertised execution capability, not as a portable persisted setting.
- `max_escalations`: integer from 0 through 4. Default to 2 if invalid.
- `max_agents`: integer from 0 through 8, additionally capped by the current host. Default to 3 if invalid. Zero forbids Pilot-managed explicit delegation; it cannot reconfigure an already active Ultra host's internal fan-out.
- `ponytail`: `auto`, `required`, or `disabled`.
- boolean fields: `true` or `false`.

If `min_reasoning` is higher than `max_reasoning`, ignore both invalid values and use the defaults unless the current prompt clearly resolves the conflict. A hard user maximum wins over Pilot's baseline; report reduced confidence when that maximum is below the reliable floor for the task.

`allow_fast = true` permits an already supported and enabled Fast mode. It does not authorize Pilot to mutate Codex settings or prove that Fast is active.

`allow_ultra = true` permits an Ultra recommendation or use when the host already exposes it. It does not activate Ultra.

## Policies

### quality

Default. Prefer strong verification and allow upper tiers, Max, or Ultra when justified. Keep reasoning at medium or above. Speed is the lowest priority.

### balanced

Prefer Luna and Terra for clear work, use Sol when complexity or risk requires it, and use high effort selectively. Fast remains off unless explicitly allowed. Ultra requires a clear multi-agent benefit.

### throughput

Prefer efficient models, single-agent execution, and the lowest permitted sufficient reasoning. Fast may be used only when explicitly allowed and already supported. Never trade away correctness to increase throughput.

## Ponytail

Ponytail is an optional separate skill or plugin. Use the host-advertised Skill instructions as the source of truth; do not copy, vendor, or reconstruct them inside Pilot.

Invoking Codex Pilot alone is sufficient. Do not require or ask the user to invoke both skills: for an implementation request, Pilot applies the setting below and loads an advertised Ponytail coding skill itself. An explicit current-request instruction to stop or disable Ponytail still wins by the precedence rules above.

- `auto`: inspect the skills already advertised by the host. For a Pilot implementation request, if a Ponytail coding skill is available, load it once after understanding the code. If the host explicitly reports that a trusted Ponytail hook already injected the active rules, do not load or restate them again. Otherwise continue silently.
- `required`: use the advertised Ponytail skill. If it is unavailable, stop before implementation and state that the required dependency is missing.
- `disabled`: do not invoke Ponytail.

Do not scan unrelated user files to discover Ponytail. A host's installed-skill/plugin listing or skill catalog is enough. If available, keep responsibilities separate:

- Codex Pilot owns routing, orchestration, verification, and escalation.
- Ponytail owns minimal implementation, reuse, and YAGNI guidance.
- `AGENTS.md` owns project-specific rules.

Ponytail does not select the model, reasoning effort, Parent upgrade, worker escalation, or agent count. Its `lite`, `full`, and `ultra` values are Ponytail intensities, not Codex reasoning levels; specifically, Ponytail `ultra` does not activate Codex Ultra.

User requirements and project rules remain authoritative. A Ponytail review may shrink the implementation, not the acceptance criteria, and must not justify omitting required tests or weakening validation, security, error handling, accessibility, readability, or a necessary abstraction. After using Ponytail, reuse that decision as Pilot's single minimality review instead of repeating a parallel checklist.
