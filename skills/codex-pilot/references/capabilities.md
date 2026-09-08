# Conditional capability requirements

Pilot specifies needs; the host's current tool descriptions determine providers and invocation. Resolve only capabilities relevant to the task. Provider names below are examples, not mandatory dependencies or verified integrations.

| Capability | Needed when | Avoid when | Example provider |
| --- | --- | --- | --- |
| semantic_navigation | Symbol references, callers/callees, class/function relationships, multi-file flow, large codebase navigation, symbol-aware refactoring materially reduce exploration | A clear local text edit needs no relationship analysis | Serena |
| current_documentation | Current framework, SDK, external API, version-dependent behavior, deprecation/replacement, or specification matters | Project-internal stable logic suffices | Context7 |
| context_compression | Large repetitive logs, build/test output, JSON, or diagnostics overwhelm useful context | Short output, exact source code, or fidelity-critical evidence | Headroom |
| security_analysis | Auth, authorization, trust-boundary input validation, injection, command execution, path traversal, uploads, crypto, secrets, sensitive data, or security migration | Ordinary business logic without security implications | Semgrep |

For current documentation, identify the project's relevant version and prefer authoritative documentation matching it. For compression, preserve access to raw output and exact errors, locations, and causal evidence; reopen originals before correctness-critical conclusions. Compression never outranks fidelity.

## Availability and fallback

A required capability is an analytical need, not a requirement for one named product. Prefer currently advertised semantic navigation when symbol relationships matter; bounded native search and source inspection may suffice. Authoritative docs lookup can replace a docs provider. Focused raw-output extraction can replace compression. Existing project analysis and targeted security tests/review may cover a security need.

Evaluate whether the fallback meets the same verification floor. Report any material gap, especially unavailable security analysis on authorization work. Continue safe work when possible; leave affected conclusions unverified if the need cannot be met. A missing irrelevant tool never blocks the task. Do not install or diagnose all providers before starting.

## Responsibility boundary

The host, its plugins, and advertised tools own installation, package/version management, APIs, and execution. Pilot owns assessment, bounded delegation, and verification depth. Do not hard-code provider tool names, add compatibility shims, pin versions, build wrappers, or implement MCP supervision.

Ponytail is optional. ast-grep is not a core capability or integration; consider it only as a future extension after comparative evidence shows value beyond semantic navigation. Record observed integrations as dated snapshots in [compatibility](../../../docs/compatibility.md), never as a permanent catalog.

Do not persist source, prompts, secrets, or routing telemetry. Use host-approved tools within the task's data and permission boundaries.
