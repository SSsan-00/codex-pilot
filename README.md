# Codex Pilot

Codex Pilot is a reusable, skills-only Codex plugin that right-sizes execution for software-development tasks. It assesses complexity, risk, uncertainty, scope, verification cost, reasoning needs, parallelism, user resource policy, Parent capability, and routing confidence before choosing a strategy.

日本語で導入・設定・利用方法を確認する場合は、[Codex Pilot 利用ガイド](docs/user-guide.ja.md)を参照してください。

> Use the least expensive computation that can solve the task reliably, without sacrificing correctness.

Codex Pilot is an instruction-based orchestrator. It uses Codex's own project inspection, model-aware subagent controls, and verification tools. It sends no routing data to an external router and has no MCP server, hook, telemetry, API key, or runtime dependency.

## Status

Version `0.2.0` targets current Codex Skill and Plugin formats. The local compatibility snapshot and verified limits are in [docs/compatibility.md](docs/compatibility.md).

The key boundary is intentional: a Skill can select an advertised model and reasoning level for a spawned worker when the host exposes those controls, but it cannot reliably detect or switch the already-running Parent. It also cannot directly turn Fast or Ultra on. Codex Pilot recommends a new Parent setting when necessary and never pretends that an advisory setting was applied.

## Architecture

The repository root is the plugin root:

```text
codex-pilot/
├── .codex-plugin/plugin.json
├── skills/codex-pilot/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── capabilities.md
│       ├── configuration.md
│       ├── escalation.md
│       └── routing.md
├── docs/compatibility.md
├── docs/user-guide.ja.md
├── evals/
├── examples/codex-pilot.toml
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

The layout follows the official [Skill](https://learn.chatgpt.com/docs/build-skills) and [Plugin packaging](https://developers.openai.com/plugins/build/plugins) formats. The Skill remains focused while conditional detail is loaded from references only when needed.

Execution flow:

```text
User request
  -> current Parent
  -> project guidance and relevant-code inspection
  -> required Ponytail pre-check
  -> task assessment and routing confidence
  -> user resource policy and capability discovery
  -> Parent execution or bounded worker delegation
  -> proportional verification and minimality review
  -> evidence-based worker escalation, if needed
  -> result
```

## Routing

Codex Pilot uses ordered gates, not a large scoring engine.

| Class | Typical work | `quality` baseline |
| --- | --- | --- |
| SIMPLE | Clear local typo, rename, or mechanical edit | Luna / medium `[Luna-2]` |
| NORMAL | Routine feature, test, refactor, or bug fix | Terra / high `[Terra-3]` |
| COMPLEX | Unresolved cause, multi-module work, DB/cache/async, difficult verification | Sol / xhigh `[Sol-4]` |
| CRITICAL | Architecture, major migration, security, data integrity, distributed/concurrent systems | Astra / max `[Astra-5]` |

High uncertainty excludes Luna. High risk plus high uncertainty or difficult verification normally requires Sol even if the eventual diff is small. `ULTRA CANDIDATE` is an annotation on COMPLEX or CRITICAL work, not a fifth class.

These labels express required capability. They do not force a worker spawn. If the capable Parent can execute a cohesive task directly, spawning a lower-tier worker may waste more context than it saves.

Exact model IDs are discovered from the current host. Codex Pilot keeps Luna, Terra, Sol, and Astra as logical display families and does not guess that one identifier is an alias of another. Visible routes append a family-relative reasoning stage: `low=1`, `medium=2`, `high=3`, `xhigh=4`, and `max=5`. For example, `[Luna-3]` means Luna / high; it is not a cross-family benchmark rank.

## Execution policies

### `quality` (default)

Strong verification; reasoning at medium or above; upper models, Max, and Ultra allowed when justified; speed is the lowest priority. The recommended Parent is Sol / high for normal orchestration and Sol / xhigh when classification and integration are themselves unusually difficult.

### `balanced`

Luna and Terra handle clear everyday work. Sol is used when complexity, risk, or uncertainty requires it. Fast remains off unless the user permits it. Ultra needs a clear parallel benefit.

### `throughput`

Prefer efficient models, the lowest permitted sufficient reasoning, and fewer agents. Throughput never means knowingly reducing correctness.

## Parent Model

The model selected when the task starts is the Parent/orchestrator. It owns task understanding, routing, delegation, result integration, verification, and escalation decisions.

A static Skill has no documented portable interface that returns the live Parent model and reasoning level. Reading `config.toml` is not detection: composer and turn-level overrides can differ. Codex Pilot uses explicit runtime metadata or a user-provided value; otherwise it records `Current Parent: unknown`.

Codex Pilot cannot change the active Parent mid-turn. When routing confidence remains low and the Parent itself is the bottleneck, it recommends the smallest useful next step, usually:

```text
Sol / high -> Sol / xhigh -> Sol / max -> Astra / high -> Astra / xhigh -> Astra / max -> Ultra
```

It tries bounded inspection first, does not jump directly to Ultra, and keeps Worker escalation separate. Downgrade suggestions are on by default, appear only after clearly SIMPLE work with a known overpowered Parent, and never interrupt the task.

## Workers, Multi-Agent, and Ultra

When the host supports explicit subagent controls, Codex Pilot supplies both the host-advertised model ID and reasoning effort. Otherwise the child may inherit the Parent or use a model default, so Pilot falls back to capable Parent execution or an advisory route.

Parallel workers receive distinct bounded roles such as code-flow analysis, architecture alternatives, or tests and edge cases. Read-heavy parallelism is preferred; write ownership is coordinated. The default Pilot cap is three agents and never increases the host's own concurrency limit.

[OpenAI's subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) defines Ultra as maximum reasoning with proactive delegation on supported models and eligible accounts. It is not a model name. If Ultra is active, Pilot avoids overlapping manual fan-out. `allow_ultra = true` permits use or recommendation; it does not activate Ultra.

## Worker escalation

Escalation follows evidence, not the first failure:

```text
Luna -> Terra -> Sol high/xhigh -> Sol max -> Astra high/xhigh/max -> Ultra candidate
```

An obvious syntax, command, dependency, or environment issue is corrected at the same tier. Contradictory evidence, an unresolved cause, underestimated impact, or low confidence on a material conclusion can justify a stronger worker. The default budget is two compute-tier escalations, so one run does not traverse the whole illustrative ladder. Each handoff carries only task facts, inspected files, changes, failed verification, remaining hypotheses, and the next check.

## Routing confidence

- `high`: scope, risk, route, and verification are clear.
- `medium`: some uncertainty remains, but it cannot change the safe route.
- `low`: scope, consequences, or result integration may change the route.

Low confidence triggers bounded investigation first. If confidence remains low because only implementation is difficult, Pilot escalates a Worker. If the Parent cannot safely classify or integrate the result, Pilot gives a short Parent upgrade recommendation and pauses before consequential edits.

## Ponytail

Ponytail remains a separate external dependency and is required by default:

- `required` (default): stop before implementation and report it missing when unavailable.
- `auto`: use it when already advertised by the host; otherwise continue silently.
- `disabled`: do not invoke it.

Codex Pilot never vendors or reconstructs an unseen Ponytail. When present, Ponytail owns minimal implementation and YAGNI review; Codex Pilot owns routing and verification; `AGENTS.md` owns project-specific rules.

Invoking Codex Pilot alone is sufficient; users do not need to add a second Ponytail invocation. For implementation requests, Pilot loads an advertised Ponytail coding skill at most once after it understands the affected code and reuses that result as its minimality review. Trusted host hooks may already inject Ponytail; Pilot does not duplicate them. Ponytail's `lite`, `full`, or `ultra` intensity changes only its minimality guidance—Ponytail `ultra` is unrelated to Codex Ultra and cannot change models, reasoning, or agents. User acceptance criteria, project rules, required tests, and safety controls always win.

Self-hosting verification used [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) v4.9.0. It is an external Plugin required by the default policy and is never installed by Codex Pilot itself. Review and trust its lifecycle hooks separately from installing or invoking its Skills.

## Fast mode

Fast is a host feature. On supported Codex surfaces, users can control it with `/fast` or supported Codex configuration as described in the official [Speed documentation](https://learn.chatgpt.com/docs/agent-configuration/speed).

There is no documented Skill or Plugin manifest control that toggles Fast for the live turn or a spawned worker. Therefore:

- `allow_fast = false` rejects Fast as a Pilot policy;
- `allow_fast = true` allows an already supported, user- or host-enabled Fast mode;
- Pilot reports Fast active only when the host exposes observable status.

## Configuration

Configuration is optional after the required Ponytail dependency is installed. Most users can then install the Skill and ask for a development task normally. If Ponytail is unavailable, the default policy stops before implementation; see [Ponytail](#ponytail) for installation or set `ponytail = "auto"` explicitly.

Precedence is per setting:

```text
current user instruction
> <repo-root>/.codex-pilot.toml
> $CODEX_HOME/codex-pilot.toml
> bundled defaults
```

The Pilot file is deliberately separate from Codex's official `config.toml`; unknown Pilot keys are never inserted into Codex configuration. Copy [examples/codex-pilot.toml](examples/codex-pilot.toml) only when persistent overrides are useful.

```toml
policy = "quality"
allow_fast = false
allow_ultra = true
min_reasoning = "medium"
max_reasoning = "max"
max_escalations = 2
max_agents = 3
ponytail = "required"
show_routing = true
suggest_parent_upgrade = true
suggest_parent_downgrade = true
```

Do not put secrets, executable commands, or tool definitions in this file. Pilot reads only the documented resource-policy keys.

## Usage

Normal use is just a development request:

```text
Fix this bug and add an appropriate regression test.
```

Implicit selection is enabled, but model-controlled description matching cannot be guaranteed for every prompt. Explicit invocation is deterministic:

```text
$codex-pilot fix this bug and add an appropriate regression test
```

Manual overrides are respected:

```text
$codex-pilot use the balanced policy, forbid Ultra, and cap reasoning at high for this refactor
```

### Route-only

A Plugin/Skill cannot guarantee an arbitrary `/pilot` slash command. Use:

```text
$codex-pilot route-only: evaluate this migration without changing files
```

Route-only returns class, required capability, agents, Ultra status, Parent recommendation, confidence, and short reason categories. It makes no file changes or mutating calls and does not reveal private chain-of-thought.

Normal completed work includes one compact routing line with a family-relative strength label in the final response by default, for example `Routing: NORMAL -> Terra / high [Terra-3] (...)`. A progress-only line is insufficient. Set `show_routing = false` to hide it.

## Installation

### Local source checkout

Clone or unpack this repository anywhere. Do not nest another `codex-pilot` directory inside it; the checkout root is already the Plugin root.

For local development, install the bundled Skill with a symlink so this checkout remains the source of truth. Codex officially discovers user skills under `$HOME/.agents/skills` and follows symlinked skill directories.

macOS, Linux, or WSL:

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/codex-pilot/skills/codex-pilot" "$HOME/.agents/skills/codex-pilot"
```

Verify that the destination does not already exist before creating the link. Do not overwrite another installation.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
New-Item -ItemType SymbolicLink `
  -Path "$HOME\.agents\skills\codex-pilot" `
  -Target "C:\absolute\path\to\codex-pilot\skills\codex-pilot"
```

Windows may require Developer Mode or elevated permission for symlinks. If symlinks are unavailable, copy that one Skill directory and repeat the copy after source updates.

Start a new Codex task and use `/skills` or explicitly invoke `$codex-pilot`. The IDE extension supports standalone skills but not Plugin browsing. Plugin installs are supported in the ChatGPT desktop app and Codex CLI; see the official [Plugins guide](https://learn.chatgpt.com/docs/plugins).

### Marketplace distribution

This repository is a valid Plugin package, not a marketplace root. A publisher or workspace admin must add it to a marketplace catalog before users can install it with `codex plugin add`. Do not run `codex plugin marketplace add` on this repository as if its root were a catalog.

Once a catalog contains Codex Pilot, install its exact entry and start a new session:

```text
codex plugin add codex-pilot@<marketplace-name>
```

Public publication requires OpenAI's plugin submission and review process. This repository intentionally contains no invented publisher, privacy-policy, terms, or repository URL.

## Uninstall and rollback

For a symlink install, first verify that `$HOME/.agents/skills/codex-pilot` is a symlink to this checkout, then remove that exact link. Do not recursively remove the source checkout or the whole skills directory. Restart Codex if the catalog does not refresh.

For a marketplace install, use its exact marketplace identity:

```text
codex plugin remove codex-pilot@<marketplace-name>
```

Delete optional `.codex-pilot.toml` files only if you created them specifically for Pilot. Installation does not overwrite `config.toml`, `AGENTS.md`, existing skills, plugins, or Ponytail, so rollback does not require restoring them.

## Privacy

Codex Pilot has no external router or telemetry and persists no routing log. If a user asks for metadata, Pilot limits it to class, selected family and advertised ID, reasoning, escalation count, reason category, and timestamp. It never stores prompt text, source text, credentials, secrets, or environment-variable values.

This statement covers Codex Pilot itself. The Codex host, selected tools, repositories, and connected services have their own data and retention behavior.

## Cross-platform support

The runtime Skill contains shell-neutral instructions and has no mandatory script.

- macOS: locally verified; see the compatibility snapshot.
- Windows Native: statically reviewed; PowerShell is preferred and POSIX tools are not assumed.
- WSL: statically reviewed as Linux; Windows and WSL paths are not translated automatically.
- Linux: statically reviewed; no OS-specific dependency is required.

Project verification commands remain project-specific and may add their own platform requirements.

## Verification

The evaluation corpus in [evals/cases.json](evals/cases.json) covers seven routing cases, four Parent recommendation cases, five escalation transitions, eight Ponytail integration cases, family-relative strength labels, final-response routing visibility, and route-only invariants. [evals/README.md](evals/README.md) defines forward-testing rules.

Before release:

1. run the official Skill validator on `skills/codex-pilot`;
2. run the official Plugin validator on the repository root;
3. run route-only cases in a clean read-only repository;
4. separate explicit invocation correctness from implicit-discovery smoke tests;
5. accept model-switching evidence only from host spawn metadata, never generated prose.

Verified results for this checkout are recorded in [docs/verification.md](docs/verification.md).

## Troubleshooting

### The Skill does not appear

Confirm the link or copied directory ends in `codex-pilot/SKILL.md`, then start a new task. Use `/skills` or `$codex-pilot`. Check for another installed Skill with the same `name`; duplicates are not merged.

### The Plugin was updated but behavior did not change

Marketplace installs run from an installed cache rather than necessarily from the source checkout. Reinstall or update the plugin through the same marketplace and start a new task. A standalone symlink avoids this cache during development.

### A requested model or reasoning level is unavailable

Availability depends on host, account, authentication, and rollout. Pilot uses the closest sufficient advertised capability within user limits and reports a material fallback.

### Pilot does not know the Parent

That is expected when live runtime metadata is not exposed. Provide the Parent family and reasoning explicitly for a route-only comparison, or use the model controls in the composer/CLI for the next task.

### Fast or Ultra was not activated

Pilot policy cannot toggle either feature. Enable a supported mode in the host, then start or rerun the task. Pilot will use observable capabilities without claiming unsupported control.

### Ponytail is unavailable

The default `required` mode intentionally stops before implementation when Ponytail is unavailable. Set `ponytail = "auto"` to continue without it, or install Ponytail as described above.

## Limitations

- No portable live Parent detection or mid-turn Parent switching.
- No Skill-level Fast toggle or proof when status is hidden.
- No direct Ultra activation; account and host support are required.
- No guarantee that implicit Skill matching fires for every ordinary prompt.
- No guarantee that every Codex surface exposes explicit child model/effort controls.
- No real-device verification yet on Windows, WSL, or Linux.
- Routing quality still depends on the Parent's ability to assess the task; low-confidence cases deliberately surface this limit.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep routing explicit and small, add regression cases for demonstrated failures, preserve capability honesty, and avoid new services or hooks unless they solve a verified gap.

## License

MIT. See [LICENSE](LICENSE).
