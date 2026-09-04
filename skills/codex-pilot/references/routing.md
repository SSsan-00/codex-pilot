# Routing rules

Read this file for every route decision. It is the single maintained map from logical task signals to execution tiers. Exact model IDs are discovered from the host and are not normalized here.

## Assessment

Assess these dimensions after inspecting enough project context to avoid classifying by prompt length or file count alone:

| Dimension | Values |
| --- | --- |
| Complexity | low, medium, high, critical |
| Risk | low, medium, high |
| Uncertainty | low, medium, high |
| Scope | local, multi-file, multi-module, system-wide |
| Verification difficulty | easy, normal, difficult |
| Required reasoning | low, medium, high, very-high |
| Parallelism benefit | none, low, medium, high |
| Routing confidence | high, medium, low |

Treat security, data integrity, destructive migrations, difficult concurrency, and externally irreversible actions as risk floors. Treat an unclear cause, ambiguous requirement, unfamiliar architecture, or contradictory evidence as uncertainty, even when the eventual diff may be small.

## Classification

Choose one primary class. `ULTRA CANDIDATE` is a flag on a COMPLEX or CRITICAL task, not a fifth complexity class.

### SIMPLE

All material signals are low: the change is clear, local, mechanical, low-risk, and easy to verify. Examples include a typo, a one-symbol rename with known references, or a few unambiguous lines.

A simple-looking task with high uncertainty is not SIMPLE.

### NORMAL

Routine feature work, ordinary bug fixes, tests, refactors, or multi-file business logic with understood scope and normal verification.

### COMPLEX

Any strong complexity signal: multi-module behavior, unresolved causes, substantial refactoring, database/cache/async interactions, material design choices, wide impact, difficult verification, or multiple plausible hypotheses.

### CRITICAL

Architecture, large migration, security-critical work, data integrity, destructive database migration, distributed systems, difficult concurrency, or critical performance where a wrong decision has a large blast radius.

Raise the class by one when high uncertainty materially affects scope or verification. High uncertainty always excludes Luna. High risk plus high uncertainty, or high risk plus difficult verification, normally requires Sol even if the apparent code change is small.

## Logical model families

Use logical families in policy decisions:

- **Luna**: efficient worker for clear, narrow, repeatable tasks.
- **Terra**: balanced worker for ordinary development and bounded investigation.
- **Sol**: flagship worker or Parent for ambiguous, complex, high-value work.

The dated [compatibility snapshot](../../../docs/compatibility.md) records the IDs seen during development. Preserve the exact ID returned by the current host. Never silently translate one host identifier into another.

The preferred Parent for the `quality` policy is Sol / high, with Sol / xhigh when the orchestration and integration itself is unusually difficult. This is a Pilot policy choice; it does not override account availability or the user's selection.

## Baselines

These are sufficiency targets before capability fallback and user limits.

| Class | quality | balanced | throughput |
| --- | --- | --- | --- |
| SIMPLE | Luna / medium | Luna / medium | Luna / medium |
| NORMAL | Terra / high | Terra / medium | Terra / medium |
| COMPLEX | Sol / xhigh | Sol / high | Terra / high only when bounded and confidence is high; otherwise Sol / high |
| CRITICAL | Sol / max | Sol / xhigh | Sol / xhigh |

Apply `min_reasoning` and `max_reasoning` after selecting the baseline. Never ask for an effort the chosen exact model does not advertise. If a lower hard maximum prevents the reliable floor, obey it, strengthen verification where possible, and report the constraint.

The baseline does not require a subagent. If the Parent is already at least as capable, the task is cohesive, and delegation would duplicate context, execute in the Parent.

## Ultra candidate gate

Set `ultra_candidate = true` only when all are true:

- the task is COMPLEX or CRITICAL;
- uncertainty or stakes are very high;
- two or more independent workstreams can be defined;
- parallel investigation is likely to improve correctness or wall-clock time enough to justify extra tokens;
- `allow_ultra` is true and the host/account exposes Ultra.

Typical candidates include a large codebase with several independent concurrency hypotheses, or a critical architecture decision that benefits from separate architecture, implementation, test, and risk reviews.

Prompt length, many files, prestige, or speed alone are not reasons to use Ultra. Max is deeper single-agent reasoning; Ultra adds proactive subagent orchestration. If Ultra is already active, avoid a second overlapping fan-out.

## Agent topology

- Parallelism `none` or `low`: use no subagent unless isolation is needed.
- Parallelism `medium`: use one or two bounded Pilot-managed agents only when their work is independent.
- Parallelism `high`: use distinct Pilot-managed roles up to `max_agents`; default cap is three. An already active Ultra host owns and controls its separate internal fan-out.

Good roles include code/dependency flow, architecture/alternatives, and tests/edge cases. Do not assign several agents to “do everything.” Give one writer ownership of each file or keep parallel agents read-only, then integrate centrally.

## Capability fallback

Discover what the current host exposes. Then:

1. Prefer the requested logical family and effort when its exact advertised ID is available.
2. If the effort is unsupported, choose the nearest supported effort within user bounds; prefer the higher value when correctness would otherwise fall below the route floor.
3. If the family is unavailable, use the nearest available family that still meets the task floor. Prefer a more capable fallback for risk or uncertainty; prefer a cheaper fallback only when it remains sufficient.
4. If explicit spawn controls are unavailable, execute with the capable Parent or describe the worker route as advisory.
5. If no permitted route meets the reliability floor, do not pretend it does. Report the limiting policy or capability and, when enabled, give the minimal Parent upgrade recommendation.

Do not probe unavailable models by repeated failing runs. One advertised capability lookup or one bounded spawn attempt is enough.

## Routing confidence

- **high**: task boundary, risk, and verification are clear.
- **medium**: some uncertainty remains, but the route and safe next investigation are clear.
- **low**: scope or risk cannot be classified reliably, evidence conflicts, or the Parent may be unable to integrate the result.

Low confidence first triggers safe, bounded inspection. If it remains low, distinguish a worker problem from a Parent bottleneck. A difficult implementation that a stronger worker can perform is worker escalation. Inability to classify or integrate the task safely is a Parent upgrade condition.

## Routing visibility

When `show_routing` is false, keep the route internal. When true, show one short line with class, logical family/effort, and a reason category. Route-only mode always shows the compact decision and never exposes hidden chain-of-thought.
