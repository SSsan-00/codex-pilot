# Verification and escalation

Read this file after a meaningful failure, unexpected scope increase, contradictory evidence, or unresolved cause.

## Verification

Discover the project's existing checks and select those proportional to the change:

- build or compile;
- focused unit tests, then broader tests when risk justifies them;
- integration tests for changed boundaries;
- lint, type check, formatter check, or static analysis already used by the project;
- diff and behavior review for the actual acceptance criteria.

Do not add a test that only mirrors a reversible implementation detail. Do not repeatedly run broad suites after they pass unless new changes or evidence justify it. For high-risk changes, independently verify rollback, data integrity, security boundaries, or concurrency assumptions as applicable.

## Correct before escalating

Fix an obvious syntax error, mistaken command, missing local dependency, or known environment mismatch directly when the current route is still sufficient. A first failure is evidence, not an automatic request for Ultra.

Escalate a worker when one of these remains after a bounded attempt:

- unexplained build, test, lint, or type-check failure;
- unresolved root cause or contradictory evidence;
- several viable hypotheses that exceed the current worker's reasoning needs;
- scope, architecture impact, security risk, data-integrity risk, or concurrency risk was underestimated;
- the diff becomes unexpectedly large or the minimality review finds unsupported complexity;
- the current worker reports low confidence on an important conclusion.

## Ladder and budget

Use the smallest step likely to address the limitation; do not visit every step mechanically:

```text
Luna -> Terra -> Sol high/xhigh -> Sol max -> Astra high/xhigh/max -> Ultra candidate
```

An effort increase on the same suitable family may be enough. Ultra additionally requires the gate in `routing.md`.

Each move to a more capable worker or materially higher effort consumes one escalation. A corrected command or a new test using the same route does not. Stop after `max_escalations` (default two), report the remaining evidence, and request direction only when no safe in-scope path remains.

## Handoff

Pass only reusable evidence:

- task and acceptance criteria;
- known facts and applicable project rules;
- inspected files and relevant symbols;
- modifications already made;
- exact failed verification and the smallest useful output excerpt;
- remaining hypotheses and uncertainty;
- recommended next check.

Do not paste whole source trees, secrets, credentials, environment variables, or unrelated logs. Let the stronger worker re-open important code needed to verify the handoff.

## Worker escalation versus Parent upgrade

Use worker escalation when the Parent can still classify, supervise, and integrate the work. Use Parent upgrade only when the Parent itself cannot reliably classify the task or reconcile the results.

For a known Parent, progress gradually where supported:

```text
Sol / high -> Sol / xhigh -> Sol / max -> Astra / high -> Astra / xhigh -> Astra / max -> Ultra
```

A weaker known Parent may first move to the next sufficient family or effort. Do not recommend Ultra unless Max is plausibly insufficient and independent parallel work has clear value. If the Parent is unknown, make the recommendation conditional and never claim the current setting is inadequate as a fact.

Keep upgrade UX short:

```text
Routing confidence: low

The task has unresolved system-wide and data-integrity risk. If the current Parent is Sol / high, rerun with Sol / xhigh before consequential changes.
```

When `suggest_parent_downgrade = true` (default), a known overpowered Parent may receive one short suggestion after a clearly SIMPLE route; never interrupt the task for a downgrade. Omit it when the Parent is unknown or the user sets this option to false.
