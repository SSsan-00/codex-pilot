# Codex Pilot evaluations

`cases.json` is the regression corpus for routing, Parent recommendations, escalation, and route-only behavior. It checks semantic decisions rather than exact prose.

## Forward evaluation

Use a fresh Codex task so the installed skill catalog is reloaded. Explicitly invoke the skill for correctness tests:

```text
$codex-pilot route-only: READMEのスペルミスを1箇所直して
```

For each `routing` case, compare the class, logical family, reasoning range, family-relative strength label, and Ultra flag. The numeric suffix is the effort ordinal within that family, never a cross-family benchmark rank. For Parent tests, supply the `parent`, completed-inspection, Parent-bottleneck, and config values as explicit test context; do not claim that the skill detected them. The requested Parent step is separate from a stronger worker floor.

Each escalation fixture is an independent transition test. Do not run all four as one default-policy chain: `max_escalations = 2` stops a single run after two tier increases unless the user explicitly raises the budget.

For `ponytail_integration`, vary advertised capability independently from config. Check invocation timing and boundaries rather than Ponytail's prose: `auto` continues when absent, `required` stops when absent, route-only never invokes it, its `ultra` intensity never activates Codex Ultra, and minimality never shrinks user acceptance criteria or required safety checks.

Route-only tests must run in a disposable clean repository with read-only permissions. Compare the file tree and Git status before and after the run, and inspect the task's tool activity. A passing run contains the required decision fields, attempts no mutating command, spawns no agent, and leaves no file change. An unchanged tree alone is insufficient because the sandbox might have blocked an attempted mutation.

Implicit activation is a separate discovery smoke test because description matching is model-controlled. Ask a representative development request without `$codex-pilot`, then inspect whether the host reports that the skill was loaded. Do not infer activation from similar wording alone.

Actual worker switching passes only when the host's spawn metadata or agent activity identifies the requested exact model and reasoning. Text saying “using Luna” is not evidence. Mark Parent switching, Fast, or Ultra activation unsupported when the host provides no control for them.
