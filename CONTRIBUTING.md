# Contributing to Codex Pilot

Thank you for improving Codex Pilot.

## Design rules

- Preserve correctness and capability honesty before cost or speed.
- Keep the Plugin skills-only unless a demonstrated need justifies another component.
- Keep current model identifiers in one compatibility location and resolve live IDs from the host.
- Do not add an external router, source-code upload, telemetry, secret, or mandatory service.
- Do not turn one failed example into a universal rule. Prefer a narrow gate and a regression case.
- Keep `AGENTS.md`, Ponytail, and Codex Pilot responsibilities separate.
- Do not claim Parent, Fast, Ultra, or model-switching control without observable host evidence.

## Change workflow

1. Explain the behavioral gap and the smallest rule that addresses it.
2. Update `SKILL.md` only for shared behavior; put conditional detail in the relevant reference.
3. Add or update a semantic case in `evals/cases.json`.
4. Run the Skill and Plugin validators.
5. Forward-test explicit invocation in an isolated read-only repository.
6. If discovery behavior changed, test implicit activation separately.
7. Update `docs/compatibility.md` only with dated, observable evidence.

Do not assert exact prose in evaluations. Check the class, capability floor, user limits, mutation boundary, escalation budget, and whether a claimed capability is observable.

## Compatibility changes

OpenAI model catalogs and Codex controls can change. Preserve host-reported identifiers, cite current official documentation, and keep older supported environments on a safe fallback. A compatibility update must not silently turn an advisory option into claimed runtime control.

## Pull requests

Keep changes focused. Describe the affected routing cases, validation performed, platform actually tested, and any remaining limitation. Never include credentials, private prompts, proprietary source, or personal absolute paths.
