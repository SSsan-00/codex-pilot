# Compatibility snapshot

This is a dated implementation snapshot, not a permanent model catalog. Codex Pilot resolves live capability from the current host and preserves exact advertised identifiers.

## Verified environment

Audit date: 2026-09-06

- Host OS: macOS (Apple Silicon environment)
- ChatGPT desktop Codex bundle: `com.openai.codex` version `26.825.31414`, build `7287`
- Active bundled CLI: `codex-cli 0.150.0-alpha.12.2`
- Active CLI path: the CLI bundled inside the desktop application
- Stable local features reported by the CLI: Skills search, Plugins, Multi-Agent, Fast mode, and hooks
- Live Parent step switching feature: reported as under development and disabled
- Ponytail: `ponytail@ponytail` v4.9.0 installed from `DietrichGebert/ponytail`; all six bundled Skills discovered in a fresh CLI prompt

An independently installed CLI may have a different version. Always use `command -v codex` (or the platform equivalent) together with `codex --version` before attributing behavior to a version.

## Skill and Plugin behavior

The current official format requires:

- `.codex-plugin/plugin.json` at a Plugin root;
- bundled skills below `skills/`;
- `SKILL.md` with `name` and `description` for each Skill;
- optional `agents/openai.yaml` for UI and invocation metadata.

Current Codex discovers repository skills under `.agents/skills`, user skills under `$HOME/.agents/skills`, admin skills under `/etc/codex/skills`, and bundled system skills. Symlinked user Skill directories are supported. A source repository's `skills/` directory alone is Plugin content, not standalone Skill discovery.

Plugin bundles are available from a new task/session after installation. Marketplace installations may run from an installed cache, so editing the source checkout does not prove the installed copy changed.

Official references:

- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Package plugins](https://developers.openai.com/plugins/build/plugins)
- [Use plugins](https://learn.chatgpt.com/docs/plugins)

## Models and reasoning

The audited local model catalog exposed these exact IDs:

| Display family | Host-advertised ID | Advertised effort | Fast advertised |
| --- | --- | --- | --- |
| Luna | `gpt-5.6-luna` | low through max | yes |
| Terra | `gpt-5.6-terra` | low through max, plus ultra | yes |
| Sol | `gpt-5.6-sol` | low through max, plus ultra | yes |
| Astra | `gpt-6-astra` | low through max | host-dependent |

Do not generalize this table to another account or release. Official pages also use identifiers such as `gpt-5.6` without documenting that it is interchangeable with `gpt-5.6-sol`. Pilot never silently normalizes those values.

Explicit read-only worker probes were accepted and host run metadata confirmed:

- Luna / medium;
- Terra / high;
- Sol / max.
- Astra availability was exposed by the current host; no live worker probe was performed for this documentation-only compatibility update.

The current orchestration interface required a context-free or bounded-history spawn for explicit model/effort overrides; a full-history inherited spawn did not accept an override. This is host behavior, not a portable Skill guarantee.

Official references:

- [Models](https://learn.chatgpt.com/docs/models)
- [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

## Parent Model detection

The development harness exposed Parent metadata for this audit, but no stable Skill API or documented environment variable makes the live Parent model and reasoning portable. The value in `config.toml` is only a layered default and can differ from a composer or turn override.

Therefore the shipped Skill uses runtime metadata only when explicitly exposed by the host. Otherwise it reports the Parent as unknown. It never reads private rollout internals as a product interface.

The audited host reported live Parent step switching as disabled. Parent upgrade remains a recommendation for a new turn/session.

## Ultra

Current official documentation describes Ultra as maximum reasoning with proactive subagent delegation on supported models and eligible accounts. It is not a model ID. The audited host supported Ultra for some models, but a Skill has no portable control to activate it. Pilot only uses an already active Ultra environment or recommends it conditionally.

## Fast

The CLI reported Fast mode as stable, and the audited model catalog advertised Fast for Luna, Terra, and Sol. The current configured service tier was `default`; live worker spawn controls had no service-tier argument.

Official controls include `/fast` on supported interactive clients and Codex host configuration. No Skill or Plugin manifest field toggles Fast for the current turn. Pilot's `allow_fast` remains a permission gate, not an activation claim. See [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed).

## Hooks and AGENTS.md

Hooks were available in the audited host, but Codex Pilot intentionally includes none. Hooks add a trust and lifecycle surface without enabling reliable Parent detection or switching. `AGENTS.md` remains the official place for project-specific rules and is not duplicated into Pilot.

Ponytail's installed Plugin declares lifecycle hooks. The complete Codex hook manifest and JavaScript sources were inspected; they read the bundled Skill, track a mode in Plugin data, and emit additional context, with no network or child-process calls. A read-only review run emitted a denied filesystem-write warning and left no `.ponytail-active` state file, so this audit does not claim that hook activation succeeded or that hooks were inactive. Persistent hook trust was not changed manually. The installed Skills work independently; Ponytail `ultra` is its own minimality intensity and is not Codex Ultra.

## Platform status

| Platform | Status |
| --- | --- |
| macOS | Live package, CLI, catalog, and symlink-discovery verification |
| Windows Native | Static path, PowerShell, and no-POSIX-assumption review; CI contract declared, not run on a real device in this audit |
| WSL | Static Linux/path-boundary review; CI contract declared, not run in WSL in this audit |
| Linux | Shell-neutral runtime review; Linux CI contract declared, not run on a real Linux host in this audit |

GitHub Actions results are not claimed until the workflow runs on GitHub.
