---
name: codex-pilot
description: Assess software-development tasks and choose sufficient execution capability, bounded delegation, and proportional verification. Use for features, fixes, refactors, investigations, and route-only development planning; not for non-development work.
license: MIT
metadata:
  short-description: Lean development execution policy
---

# Codex Pilot

Decide what execution needs; let the Codex host decide how tools run. Prioritize correctness, reliability, sufficient reasoning, verification, maintainability, context/token efficiency, cost, then speed. Cheap computation is not an end in itself.

## Assess and execute

1. Honor user instructions, resource limits, and project guidance. Enter route-only below immediately when requested.
2. Inspect only enough relevant code and project-native checks to understand complexity, risk, uncertainty, and scope. Use the class and verification table in [routing.md](references/routing.md); do not perform an elaborate scoring exercise for clear tasks.
3. Choose the sufficient capability floor, then identify task-specific needs using [capabilities.md](references/capabilities.md) only when external capabilities matter. No external capability is required for a clear README typo.
4. Execute in the Parent when work is cohesive. Delegate only independent bounded work that benefits from isolation or parallelism: one investigation means one worker; several justify a small fan-out. Prefer read-only roles and explicit file ownership. Default maximum is two Pilot-managed workers across the task, including retries, capped by the host. Zero forbids explicit workers. Respect already-active host orchestration without duplicating its fan-out.
5. Prefer the smallest sufficient change. Reuse existing abstractions before introducing new ones. Never reduce acceptance criteria or necessary safety checks for minimality. Ponytail may supplement this when available; its absence never blocks Pilot.
6. Run proportional verification and inspect the diff. Report the result and material limitations.

## Capability honesty and failures

Use only model IDs and effort values advertised by the current host. Choose both explicitly when worker controls support them; otherwise use a capable Parent or report the limitation. The route is a sufficiency recommendation, not proof of the executing model. Do not infer live Parent settings from disk configuration or claim to switch the running Parent.

Use already-active host modes within user limits. Fast and Ultra belong to the host; Pilot adds no activation logic, installer, updater, adapter, daemon, or service.

Correct obvious command or syntax errors directly. After a meaningful unresolved failure, allow one stronger bounded retry only when evidence suggests it can help and user/agent limits permit it. Carry facts, changed files, failed checks, and the next hypothesis; do not restart a mechanical model ladder. If the reliable floor still cannot be met, report the limitation and unfinished checks; continue safe useful work, but do not claim completion of blocked work. Do not routinely request Parent upgrades or downgrades.

## Completion integrity

Use a completion claim only when requested acceptance criteria are met, relevant verification passed or the user explicitly waived it, required analysis has a verified sufficient fallback, and no material risk remains unresolved. If any condition fails, report `Status: partial` or `Status: blocked`, name the unmet condition and the next safe check, and do not use “complete”, “done”, “fixed”, or equivalent language. A weak Parent, an unavailable stronger worker, a hard user limit, a failed check, or an unavailable required capability never turns an unverified conclusion into completion.

## Configuration

Defaults: `policy = "quality"`, `max_agents = 2`, `show_routing = true`. Read [configuration.md](references/configuration.md) only for overrides or migration. Never modify host configuration to apply Pilot policy.

## Route-only

Classify the proposed task from the supplied description. Do not inspect target files, reproduce bugs, execute investigation tools, diagnose dependencies, mutate files, solve the task, or spawn workers. Reading Pilot policy is allowed. If information is missing, state uncertainty in the short reasons rather than starting investigation.

Return only class, recommended execution capability, required capabilities (or `none`), agent recommendation, optional confidence, and short reason categories:

```text
Classification: COMPLEX
Recommended: strong capability
Capabilities: semantic_navigation, current_documentation
Agents: 1 bounded investigator
Reasons: multi-module impact; version-dependent behavior
```

## Finish

Report implementation, verification, and material capability limitations without hidden reasoning. Apply the completion-integrity gate before writing the result. Unless `show_routing = false`, end with one standalone line: `Routing: COMPLEX -> strong capability`. An observed host mapping may use a family/effort such as `Sol / xhigh`; never add custom strength ordinals. Append `| Capabilities: ...` only for capabilities actually used. Report a required but unavailable capability separately in prose, not as used. When explicit workers ran, append compact `| Workers: role=host-model-id / effort` entries using observed metadata; unknown values remain `unknown`. Omit unused sections. Route-only uses its summary instead.

See [evaluations](../../evals/README.md) for semantic checks and comparison methodology.
