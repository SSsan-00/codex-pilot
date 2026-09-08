# Codex Pilot

Codex Pilot 0.4.0 — **Lean Execution Policy** — is a skills-only development execution policy. It decides how much capability, investigation, delegation, and verification a task needs.

Priority: correctness → reliability → sufficient reasoning → verification → maintainability → context/token efficiency → cost → speed. Routing overhead must earn its place; using a cheaper model is not the goal.

[日本語の利用・更新ガイド](docs/user-guide.ja.md)

## Lean architecture

```text
User → task assessment (complexity, risk, uncertainty, scope)
     → execution floor + required capabilities + bounded delegation
     → Codex host and available tools → implementation → verification
```

Pilot owns requirements and verification depth. The host owns tool execution, model controls, installation, and updates. No router service, daemon, MCP manager, API adapter, runtime dependency, or telemetry is included.

## Task classes and execution policy

| Class | Typical work | Sufficient execution |
| --- | --- | --- |
| SIMPLE | Clear local low-risk edit with easy verification | efficient |
| NORMAL | Understood feature, bug, test, or refactor | balanced |
| COMPLEX | Unresolved cause, multiple modules, DB/async interaction | strong |
| CRITICAL | Architecture, security, data integrity, destructive migration, difficult concurrency | strongest sufficient available |

Small diffs do not erase risk or uncertainty. File count and prompt length alone do not raise a class. Exact model IDs and reasoning values come only from the current host. A displayed floor is a recommendation, not evidence that the running Parent changed.

Keep cohesive work in the Parent. Use one worker for one useful independent investigation and a small fan-out for several; default maximum is two workers across the task, including retries. Prefer read-only roles and separate write ownership. One meaningful unresolved failure may justify one stronger bounded retry, never an automatic ladder.

## Capability requirements

| Need | Conditional use | Example provider |
| --- | --- | --- |
| semantic_navigation | Symbol relationships, callers/callees, multi-file code flow | Serena |
| current_documentation | Current or version-dependent framework/SDK/API behavior | Context7 |
| context_compression | Large repetitive diagnostics with raw evidence preserved | Headroom |
| security_analysis | Auth, trust boundaries, injection, secrets, sensitive data | Semgrep |

These are provider examples, not verified integrations or mandatory installations. A README typo requires none. Use advertised tools or a sufficient native fallback; report material gaps when required analysis cannot be completed. Do not compress exact code or fidelity-critical evidence. ast-grep is a future evidence-gated extension, not core.

See [capability policy](skills/codex-pilot/references/capabilities.md). Pilot contains no external tool installer, updater, version pinning, proxy, or tool-name shim.

## Verification

Use project-native focused checks for small work, relevant tests/checks for normal work, broader checks when complex work justifies them, and independent checks of critical assumptions for critical work. Independence may come from another check or evidence source; it does not mandate workers. Do not rerun passed heavy suites without new evidence.

Prefer the smallest sufficient change and existing abstractions without reducing acceptance criteria. Ponytail is an optional enhancement; absence never blocks Pilot.

## Usage

```text
$codex-pilot fix this bug and verify the affected behavior
$codex-pilot route-only: assess this authorization migration
```

Implicit invocation remains enabled but is model-dependent. Route-only classifies the supplied proposal without target-file inspection, investigation, mutation, or agent spawning.

Final execution responses normally end with a compact recommendation:

```text
Routing: COMPLEX -> strong capability | Capabilities: semantic_navigation
```

Only actually used capabilities appear. Missing required capabilities are reported separately. Actual explicit workers retain compact model/effort entries without custom ordinal labels. Set `show_routing = false` to hide the execution line.

## Optional configuration and migration

```toml
policy = "quality"
max_agents = 2
show_routing = true
```

Quality prioritizes uncertainty coverage; balanced avoids extra work after reliability is met; throughput favors fewer calls and cohesive execution at the same reliable floor. Current user instructions override repository settings, user settings, and defaults.

Version 0.4 replaces the 0.3 configuration and output contract. Legacy keys are ignored; move former resource limits into explicit task instructions or host settings. Parent upgrade/downgrade suggestions, multi-step escalation, custom strength labels, and required Ponytail are removed. The worker default is now two. See [configuration and legacy keys](skills/codex-pilot/references/configuration.md).

## Installation

From a source checkout, link `skills/codex-pilot` into your user skill directory. Check the destination does not exist first.

macOS / Linux / WSL:

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/codex-pilot/skills/codex-pilot" "$HOME/.agents/skills/codex-pilot"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
New-Item -ItemType SymbolicLink -Path "$HOME\.agents\skills\codex-pilot" -Target "C:\absolute\path\to\codex-pilot\skills\codex-pilot"
```

If links are unavailable, copy the skill folder and recopy after updates. Start a new task to load changes. This repository is a plugin package, not a marketplace catalog; marketplace users must use an existing catalog entry and the host's installation/update mechanism.

## Documentation and evidence

- [User guide and migration](docs/user-guide.ja.md)
- [Dated host snapshot](docs/compatibility.md)
- [Verification results and limits](docs/verification.md)
- [Semantic evaluations and ablation protocol](evals/README.md)
- [Contributing](CONTRIBUTING.md)

No token savings or accuracy improvement is claimed without controlled comparison. Pilot persists no routing log; host and provider data policies remain separate.
