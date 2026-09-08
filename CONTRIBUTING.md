# Contributing

Keep Pilot a thin development execution policy: assessment, sufficient capability, bounded delegation, and proportional verification. Tool installation, updates, API invocation, and execution modes belong to the host.

Before adding a core rule or integration, demonstrate a semantic failure and compare Baseline versus Feature enabled using [the evaluation protocol](evals/README.md). No measured benefit means no new core feature. Favor removing duplication; preserve correctness, user limits, and capability honesty.

Update relevant decision cases, run `python3 -m unittest discover -s tests -v`, run available Skill/Plugin validators, then forward-test in a fresh isolated read-only task. Check behavior and attempted tool activity, not exact wording or only a clean Git tree. Test implicit discovery separately when changed.

Record dated observations and limitations in [compatibility](docs/compatibility.md) and [verification](docs/verification.md). Never claim live integrations, model switching, performance savings, or remote CI from static checks. No custom installers, adapters, supervisors, benchmarks ranks, services, or telemetry.
