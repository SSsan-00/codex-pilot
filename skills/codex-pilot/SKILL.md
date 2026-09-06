---
name: codex-pilot
description: Route and orchestrate software-development tasks across available Codex models, reasoning levels, and subagents. Use for bug fixes, features, refactors, migrations, architecture, debugging, and route-only execution planning when computation should be right-sized without reducing correctness. Do not use for non-development work or when the user explicitly chose a different orchestration workflow.
license: MIT
metadata:
  short-description: Capability-aware Codex development orchestration
---

# Codex Pilot

Choose the least expensive computation that can solve the task reliably without sacrificing correctness. Preserve this priority order unless the user's resource policy changes it: correctness, reliability, sufficient reasoning, verification, maintainability, token and compute efficiency, cost, then speed.

## Start

1. Honor the user's explicit model, reasoning, Fast, Ultra, agent, route-only, and resource limits. Never silently override them.
2. Unless an override is stated or a known Pilot config is present, use the compact defaults: `quality`, Fast off, Ultra allowed, reasoning `medium..max`, two escalations, three agents, Ponytail required, visible compact routing, and Parent upgrade and downgrade suggestions on. Read [configuration.md](references/configuration.md) only to resolve an override, config file, or Ponytail dependency. Do not modify Codex configuration merely to apply Pilot policy.
3. Use the project instructions already loaded by Codex. Inspect relevant project guidance, code, dependencies, and verification commands before classifying work. Do not copy project rules into this skill.
4. For implementation work, after understanding the relevant code, apply the Ponytail integration in [configuration.md](references/configuration.md). The user does not need to invoke Ponytail separately. Skip Ponytail in route-only mode.
5. Assess complexity, risk, uncertainty, scope, verification difficulty, required reasoning, parallelism benefit, and routing confidence. Read [routing.md](references/routing.md) for the decision rules and current logical tiers.

Keep the detailed assessment internal. When `show_routing` is true, expose only the compact routing line defined below; route-only mode exposes only its compact decision summary. Never reveal private chain-of-thought.

## Tell the truth about capabilities

- Treat display families such as Luna, Terra, Sol, and Astra separately from exact model identifiers. Use exact identifiers advertised by the current host; do not invent aliases or assume availability.
- Specify both model and reasoning when the active subagent interface supports both. If it does not, treat the route as advisory and use the safest available fallback.
- A static skill cannot reliably infer the live Parent model or reasoning from a config file. Use only explicit runtime metadata or a user-provided value; otherwise record them as `unknown`.
- Do not claim to change the already-running Parent. Recommend a Parent change only when the Parent is the bottleneck and the recommendation rules below apply.
- Ultra is a maximum-reasoning, proactive multi-agent mode, not a model name. Do not claim to activate it from this skill.
- `allow_fast` is permission to use an already available, user- or host-enabled Fast mode. It is not a Fast toggle. Never edit configuration or claim Fast is active without observable host evidence.

Read [capabilities.md](references/capabilities.md) when availability, Parent detection, Fast, Ultra, installation surface, or model identifiers affect the task.

## Route and execute

Use [routing.md](references/routing.md) to select a baseline and then apply, in order:

1. user overrides and hard resource limits;
2. uncertainty, risk, and verification floors;
3. host-advertised model and reasoning capabilities;
4. the smallest sufficient agent topology;
5. a verification plan proportional to the change.

For work that fits the capable Parent and does not benefit from isolation, execute in the Parent instead of spawning a worker solely to match a lower-cost tier. The selected worker tier expresses sufficiency, not a requirement to delegate every task.

Delegate only bounded, independent work. Give each agent one distinct role, such as code-flow exploration, architecture alternatives, or test and edge-case review. Prefer read-heavy parallel work; coordinate write ownership explicitly. Never create more than `max_agents` Pilot-managed explicit workers. This setting does not control an active Ultra host's internal fan-out.

If the runtime is already Ultra, let its orchestration own fan-out. Do not create a duplicate agent tree unless the host explicitly requires delegation and the roles remain non-overlapping.

Implement the requested change, run project-provided checks proportional to risk, inspect the diff, and apply the configured minimality review.

## Parent upgrade gate

First reduce uncertainty with safe inspection. Recommend a Parent upgrade only when all are true:

- routing confidence remains low;
- the Parent's classification or result-integration ability is the bottleneck, rather than only a worker capability;
- the live Parent model and effort are known, or the recommendation is explicitly conditional;
- a minimally higher supported setting is likely to change the outcome.

Prefer the next sufficient step: higher effort on the same capable Parent before a stronger Parent, Astra before Ultra when advertised and sufficient, and Max before Ultra. Recommend Ultra only when independent parallel investigations materially help. If this gate fires before consequential edits, stop and give the user a short recommendation. Do not expose internal reasoning.

Do not suggest a Parent downgrade unless `suggest_parent_downgrade` is true. Parent recommendations never substitute for worker escalation.

## Failures and escalation

Read [escalation.md](references/escalation.md) after a meaningful verification failure, contradictory evidence, unexpected scope, or unresolved cause. Do not escalate for one obvious syntax or environment error that can be corrected directly. Count at most `max_escalations`, and carry a compact evidence handoff instead of restarting from zero.

## Route-only mode

Enter route-only mode when the user says `route-only`, asks only for routing, or uses an equivalent request. Treat the described task as a proposed task: classify what the user supplied without locating, reproducing, spell-checking, testing, or otherwise solving it. Do not read target files merely to confirm that a stated typo, bug, or change exists. Inspect project guidance or a small amount of code only when the description lacks information that could materially change the safe route. Do not modify files, run mutating commands, or spawn agents.

Return only a concise decision summary:

```text
Classification: COMPLEX
Recommended: Sol / xhigh [Sol-4]
Agents: 1-2 bounded investigators
Ultra: unnecessary
Parent upgrade: unnecessary
Routing confidence: medium
Reasons: multi-module impact; unresolved cause; difficult verification
```

Use logical family labels and the family-relative strength label defined in `routing.md`. Include an exact model ID only when the host advertised it. If the Parent is unknown, say so rather than guessing.

## Finish

Normally report the implementation and verification, not the hidden routing process. Before completing, resolve `show_routing` (default `true`). When true, the final response must end with exactly one standalone line such as `Routing: NORMAL -> Terra / high [Terra-3] (multi-file business logic change)`. If Pilot started explicit workers, append each worker's role, exact host-reported model ID, reasoning, and family-relative strength to that same line, for example `| Workers: tests=gpt-5.6-luna / medium [Luna-2]`. Include only workers actually started during the task; omit the section when none were started, and report `unknown` rather than inferring metadata the host did not expose. The bracketed label is the selected family's reasoning stage, not a cross-family benchmark rank. Do not emit that line only in commentary or progress updates; a final response without it is incomplete. When false, omit it. Route-only mode uses its decision summary instead of this line.

State any material capability fallback: unavailable requested model, unsupported effort, unknown Parent, Fast not observable, Ultra not controllable, missing required Ponytail, or exhausted escalation budget.

For representative decisions and regression prompts, see [the evaluation corpus](../../evals/cases.json).
