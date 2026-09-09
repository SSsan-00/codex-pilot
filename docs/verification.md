# Verification records

## 2026-09-10 policy refinement

Source version: 0.4.2. Completion now accepts direct analysis as well as sufficient fallbacks, requires evidence for final changes, separates waived checks from passes, and permits accurate scoped results. Unknown Parent metadata alone does not block verified work. Evidence/policy reuse and affected-check reruns reduce avoidable repetition.

Two fresh-context evaluators were requested with the same advertised model/effort (`gpt-5.6-luna` / medium), one per description. Their effective runtime settings were not independently inspected. Each simulated selection on the same 12 prompts without receiving expected answers, then examined eight completion/context scenarios against the updated policy. This is a small semantic comparison, not a randomized repeated benchmark or live implicit-discovery test.

| Prompt group | Current description | Candidate description |
| --- | --- | --- |
| Single README typo, comment formatting (2) | skip both | skip both |
| Understood heading rename in 30 docs, known one-line error explanation (2) | load both | skip both |
| Authorization, unknown cause, destructive migration, conflicting requirements (4) | load all | load all |
| Routine feature, DB/async bug (2) | load both | load both |
| Explicit typo and explicit route-only typo (2) | load both | load both |

The candidate is adopted narrowly for clear low-risk text edits and known trivial explanations requiring no investigation. This observed two fewer selections in one simulated sample; it does not establish reduced real token usage or unchanged development correctness. Explicit invocation remains supported for every development class. The 12 prompts are retained in the corpus for regression and future live testing.

Both evaluators allowed evidence-backed direct analysis and no-analysis typo completion; rejected a known failing authorization check despite a waiver; required affected checks after changes; rejected unsupported worker assurances; and disclosed unfinished scope when routing was hidden. They called for missing source recovery. One gave ambiguous status reasoning for already-present policy; the other explicitly reused it. Partial/blocked distinctions depended on available safe next work. A focused follow-up confirmed used security analysis belongs in Routing even when no fallback was needed.

Static tests check package/corpus consistency, links, and removed contracts. The old completion test only searched for specific words; it was replaced by the above behavioral evaluation and eight additional scenarios. Passing structural checks is not evidence of error-free model behavior.

Unverified: repeated live selection trials, actual implementation A/B outcomes, total token/cost savings, external provider integrations, and remote CI. No publication is part of this refinement.

## Historical 0.4.0 validation

Date: 2026-09-09. Local source changes only; no release, tag, push, or publication was performed.

## Structure and format

Passed Python standard-library contract tests for package layout, configuration/corpus consistency, relative Markdown target files, and removed runtime contracts. Both installed Skill Creator and Plugin Creator validators passed using the existing temporary validation environment; Pilot has no Python/PyYAML runtime dependency. Git whitespace checks passed.

Removed settings remain only in migration documentation and legacy-case fixtures. Runtime strength ordinals, mandatory Ponytail behavior, and Parent recommendation ladders are gone. Verification/retry guidance from the deleted escalation reference was consolidated into the Skill and routing reference. The deleted file is recoverable from Git history.

## Independent semantic evaluation

A fresh no-history evaluator read the updated Skill and its policy references, without expected corpus answers. It evaluated all 18 proposed tasks and 17 simulated behavior prompts. It reported no target-file inspection, mutations, external provider execution, or nested agent spawning. This was read-only semantic forward testing, not a live implementation benchmark or a fresh CLI installation test.

Initial class agreement: 16/18. Two clear local calculation tasks admitted SIMPLE as well as NORMAL. One unfamiliar-subsystem case selected semantic navigation where the original rubric required none; architecture added it conditionally. These exposed underspecified fixtures rather than demonstrated unsafe execution. The corpus now permits the two class alternatives only under stated low-risk conditions and explicitly permits conditional navigation for the two investigation/design cases. This post-review rubric alignment is not an independent second-run pass rate.

The 17 simulated prompts covered irrelevant missing providers, unmet and fallback security needs, raw-evidence recovery, cohesive work, zero worker limits, exhausted retry, syntax errors, unknown model metadata, hard limits, missing Ponytail, legacy limits, passed heavy checks, hidden routing, unknown worker metadata, and active host fan-out. Responses were consistent with the policy. Simulation does not establish real provider or worker behavior.

The corpus additionally specifies live/output cases including one independent investigator and exact final routing placement. Those execution-side scenarios have not all been exercised against disposable runnable projects.

A second fresh-context worker received only the Skill path and a README-typo route-only request. It returned SIMPLE, efficient sufficient capability, no required capabilities, zero agents, and short reasons. The evaluator reported two read-only calls for the Skill and routing reference only, no target inspection, mutation attempts, or nested workers. This confirms the observed response shape with self-reported tool boundaries; it is not an independently audited CLI sandbox/digest test.

## Scale

Compared with source commit 7297270:

| Measure | Before | After |
| --- | ---: | ---: |
| Tracked package files (excluding deleted file after change) | 19 | 18 |
| SKILL.md lines | 93 | 52 |
| Reference files | 4 | 3 |
| Reference lines | 334 | 73 |
| Supported configuration keys | 11 | 3 |

Line reduction is not a token-use or correctness benchmark. Evals intentionally grow in coverage while runtime policy shrinks.

## Not verified

No controlled no-Pilot/Pilot ablation, measured token savings, development correctness improvement, new live model override probe, implicit discovery test, marketplace cache refresh, external provider integration/version test, Windows/WSL/Linux device test, or remote CI run. Route-only tool prohibitions were checked in the independent evaluation but not in a new CLI sandbox/digest run. Full experimental protocol and remaining corpus scenarios are in [evals](../evals/README.md).

The compatibility document records only dated advertised capabilities; historical live claims remain in Git history.
