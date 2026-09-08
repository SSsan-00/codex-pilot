# Semantic evaluations and ablation

The corpus separates 18 task decisions from 21 behavioral scenarios. Expected values are rubrics, not a deterministic runtime router. Contract tests validate structure and consistency; they do not prove model behavior.

## Forward evaluation

Use a fresh evaluator with the updated Skill and only prompts/context, withholding expected answers. Compare class, sufficient floor, relevant capability needs, verification depth, and behavioral boundaries semantically. A provider name is not a requirement, and an unavailable required capability is not a used capability.

For route-only, use an isolated read-only task and inspect tool activity as well as before/after state. Reject attempted target investigation, mutation, dependency diagnostics, task solving, or nested worker spawning even if the sandbox blocked them. Allow reading Pilot policy. An unchanged tree alone is insufficient.

For execution scenarios, provide a disposable fixture or explicit simulated host state. Record whether the test was simulated or live. Require actual host metadata for claims of worker model/effort use. Test missing irrelevant providers, sufficient fallbacks, unmet security needs, raw-evidence recovery, worker limits, one stronger retry, and hidden routing. Report untested cases instead of treating fixture assertions as behavioral passes.

Run package checks with:

```sh
python3 -m unittest discover -s tests -v
```

Run available Skill Creator and Plugin Creator validators too. Keep implicit discovery separate from explicit invocation correctness.

## Baseline vs Feature enabled

For every proposed core addition, compare Baseline versus Feature enabled. Include no-Pilot vs lean-Pilot for overall overhead, and lean-Pilot with one capability disabled vs enabled for individual contributions. Keep task fixtures, model/effort, tool availability (except the ablated feature), acceptance criteria, and budgets matched. Use fresh sessions, alternate order, repeat runs, and score correctness without exposing condition labels where practical.

Record correctness, verification pass rate, token/context usage, tool calls, turns, unnecessary diff size, escalation count, and elapsed time where measurable. Preserve failures and denominator counts; separate total tokens from billing cost, and setup overhead from execution. Report medians, variation, sample size, environment, and unavailable metrics. Token reduction with lower correctness is not a win.

Semantic tests check policy decisions; runnable task fixtures measure development outcomes. Do not infer token savings from fewer Markdown lines. Admit a feature to core only when comparisons show meaningful benefit without sacrificing correctness; otherwise leave it out or as an extension. ast-grep requires such evidence before any integration.

Results and unverified areas belong in [verification](../docs/verification.md). No benchmark improvement is currently established.
