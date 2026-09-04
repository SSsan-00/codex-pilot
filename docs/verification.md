# Verification report

Verification date: 2026-09-05

This report distinguishes structural validation, model behavior, host metadata, and untested platform claims.

## Package validation

Passed:

- seven cross-platform contract tests, including six Ponytail integration invariants, with Python 3.11 standard library;
- the bundled Skill Creator `quick_validate.py` validator;
- the bundled Plugin Creator `validate_plugin.py` validator;
- JSON and TOML parsing through the contract tests;
- relative reference and package-path checks;
- checks for personal absolute paths, unfinished placeholders, and secret-like tokens.

The two official validators require PyYAML. It was installed only into a temporary validation virtual environment; Codex Pilot itself has no Python or PyYAML runtime dependency.

## Tested snapshot identity

After the final fixes, all validators and the final explicit route-only run were executed against this 18-file source snapshot (the report itself is excluded so recording the value does not make the digest self-referential):

```text
sha256: f76a683fffc34dde77ba091a252b7c3a03f944347e04eceaf0e38ff917b77102
```

The reproducible algorithm walks regular files below the repository root, excludes `.git`, every `__pycache__` directory, `*.pyc`, and `docs/verification.md`, and sorts POSIX relative paths. For each file it appends `UTF8(relative_path)`, a NUL byte, the 32-byte SHA-256 of the contents, and a newline to an outer SHA-256 stream. The included manifest is:

```text
.codex-plugin/plugin.json
.github/workflows/ci.yml
.gitignore
CONTRIBUTING.md
LICENSE
README.md
docs/compatibility.md
docs/user-guide.ja.md
evals/README.md
evals/cases.json
examples/codex-pilot.toml
skills/codex-pilot/SKILL.md
skills/codex-pilot/agents/openai.yaml
skills/codex-pilot/references/capabilities.md
skills/codex-pilot/references/configuration.md
skills/codex-pilot/references/escalation.md
skills/codex-pilot/references/routing.md
tests/test_contract.py
```

This digest makes the tested source set reproducible. Git history and the public remote provide the immutable publication anchor after release.

## Installation and recognition

The source repository remains the source of truth. The bundled Skill was installed as a symlink:

```text
$HOME/.agents/skills/codex-pilot -> <checkout>/skills/codex-pilot
```

The target was checked for both an existing filesystem entry and a dangling symlink before creation. No existing installation was overwritten.

The bundled CLI's prompt-construction diagnostic then listed:

```text
codex-pilot:codex-pilot ... (file: $HOME/.agents/skills/codex-pilot/SKILL.md)
```

This proves standalone Skill discovery. Codex Pilot itself is not marketplace-installed; its source-linked installation did not modify Codex config.

Ponytail was installed separately from its upstream Git marketplace as `ponytail@ponytail` v4.9.0. A fresh prompt-construction diagnostic discovered `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, and `ponytail-help`. The full Codex hook manifest and JavaScript sources were reviewed. A read-only review run emitted a denied filesystem-write warning and created no Ponytail state file, so hook activation is not claimed; persistent hook trust was not changed manually.

## Explicit and implicit invocation

Fresh `codex exec --ephemeral --sandbox read-only` sessions were run with Luna / medium.

- Explicit `$codex-pilot route-only` invocation loaded the installed `SKILL.md` and routing reference and returned `SIMPLE -> Luna / medium`, zero agents, no Ultra, no Parent upgrade, high confidence.
- A prompt without `$codex-pilot` but containing a route-only development request implicitly selected Codex Pilot, loaded the same files, and returned the same semantic decision.

Before and after the implicit run, a digest of every repository file outside `.git` and Python caches was identical:

```text
1461ca6ccc8287014a66df083a70ed5e0c93c40c4c721d443501dc31232af1d2
```

Git status was also unchanged. The run's tool activity was inspected as well: it read the installed Skill and routing reference, attempted no mutating command, and spawned no agent. The combination checks both intent and resulting state; an unchanged digest alone would not prove that the sandbox did not block an attempted mutation.

The first explicit live evaluation over-inspected the README and used 31,985 tokens. The Skill was tightened so a clear route-only description is classified as a proposed task without reproducing or solving it. The repeated explicit run used 9,332 tokens, and the implicit run used 9,206 tokens. Those totals include the host prompt and Skill loading; the final runs read only the Skill and routing rules, not the target README.

A final post-fix explicit run used JSON event output. Its only tool activity was two read-only `sed` commands for `SKILL.md`, `routing.md`, and `capabilities.md`; no mutation command or agent event occurred. It returned `SIMPLE -> Luna / medium`, zero agents, no Ultra, no Parent upgrade, and high confidence.

After Ponytail installation and integration changes, route-only was rerun from the source-linked Skill with the Ponytail catalog present. JSON events showed only read-only access to Pilot's Skill and routing/capability references: no Ponytail Skill read, mutation, or agent spawn occurred. This verifies that Ponytail availability does not override route-only isolation.

## Ponytail self-hosting

Ponytail `full` was applied to Codex Pilot's own update. It removed Pilot's copied seven-step minimality checklist, reused the upstream Skill as the single source of minimality guidance, and added only semantic boundaries with demonstrated ambiguity: one-shot invocation, scope and safety preservation, route-only exclusion, absent/required behavior, and Ponytail `ultra` versus Codex Ultra. No Ponytail code, hook, runtime, or mandatory dependency was added to this repository.

A fresh explicit review session loaded both the source-linked `codex-pilot` Skill and the installed `ponytail-review` Skill. Its first pass found duplicated Ponytail policy in `SKILL.md` and `configuration.md`; after moving the detail to the reference, the second pass returned `Lean already. Ship.`

## Routing corpus

Independent read-only forward evaluation produced:

| Case | Result |
| --- | --- |
| README typo | SIMPLE, Luna / medium, high confidence |
| One-character variable rename | SIMPLE, Luna / medium, high confidence |
| Small validation plus unit test | NORMAL, Terra / high |
| Unknown NullReferenceException | COMPLEX, Sol / xhigh |
| Large PHP-to-C# architecture migration | CRITICAL, Sol / max, Ultra scope-dependent |
| Difficult multi-source concurrency bug | CRITICAL, Sol / max, Ultra candidate only if the full gate, including host/account capability, passes |
| Small but ambiguous compatibility change | COMPLEX, Sol / xhigh in the observed run; Luna excluded |

The seventh case permits NORMAL or COMPLEX as long as the high-uncertainty floor excludes Luna and selects Terra or stronger.

## Parent recommendations

With Parent data supplied explicitly as test context:

- Sol / high plus completed bounded inspection, low confidence, and a confirmed Parent integration bottleneck produced the next Parent recommendation Sol / xhigh.
- Sol / xhigh under the same gate produced Sol / max next. Ultra remains a later option only if Max is plausibly insufficient and the complete Ultra gate passes.
- Sol / max on a README typo showed no downgrade when the default flag was false.
- With downgrade suggestions enabled, the same case allowed a short future-run suggestion without interrupting current work.

When Parent metadata was omitted, evaluators reported Parent unknown and did not claim a detected upgrade need.

## Escalation

The four fixture transitions were checked independently:

```text
Luna -> Terra
Terra -> Sol
Sol / xhigh -> Sol / max
Sol / max -> Ultra candidate, only with the complete Ultra gate
```

They are not one default-policy chain. A single run stops after the default two tier escalations unless the user raises the budget.

## Actual worker model and reasoning controls

Read-only workers were explicitly spawned, and host run metadata—not their prose—confirmed:

- `gpt-5.6-luna` / medium;
- `gpt-5.6-terra` / high;
- `gpt-5.6-sol` / max.

The audited Parent and inherited audit workers ran as Sol / ultra. Explicit child overrides on this host required a context-free or bounded-history spawn. This verifies local Worker switching but is not a promise that every Codex surface exposes the same spawn schema.

## Parent, Ultra, Fast, and Ponytail

- Development-harness metadata identified the current audit Parent as Sol / ultra. No stable Skill API exposes that value, so the shipped Skill does not scrape or depend on it.
- Parent switching was unavailable in the active host feature set. Recommendations apply to a new turn/session.
- Ultra was available to the host for supported models and treated as maximum reasoning plus proactive delegation, not a model. Pilot did not attempt to activate it.
- Fast capability was advertised, while the configured service tier was `default` and worker spawn had no Fast argument. Because Pilot defaults to `allow_fast = false`, no Fast run was attempted.
- Ponytail v4.9.0 was installed and all six Skills were discovered. Pilot's `auto` mode can now use the main coding Skill; the new corpus verifies one-shot invocation, absent/required fallbacks, route-only exclusion, scope preservation, and the distinction between Ponytail `ultra` and Codex Ultra.

## Platform status

- macOS: live CLI, package validation, Skill symlink, discovery, explicit invocation, implicit invocation, route-only zero-write, and model/effort probes passed.
- Windows Native: PowerShell and path behavior were statically reviewed; CI is declared but no real Windows device was used.
- WSL: path-separation and shell-neutral runtime were statically reviewed; no live WSL run.
- Linux: shell-neutral runtime and CI definition were statically reviewed; no live Linux run.

GitHub Actions status is checked after publication; this local report does not claim a remote result before that workflow finishes.

## Git state

The current directory was verified empty before initialization, initialized directly as a Git repository on `main`, and contains no nested `codex-pilot/codex-pilot` source tree. Publication uses the authenticated owner's `SSsan-00/codex-pilot` public GitHub repository and preserves this directory as the repository root.
