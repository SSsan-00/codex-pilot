# Compatibility snapshot

## Observed 2026-09-09

This records only the current development session's advertised interfaces, not a permanent model catalog or an end-to-end integration certification.

- Host environment: macOS, local source checkout.
- Worker interface advertises explicit model and reasoning controls; full-history forks inherit settings, bounded/no-history forks accept overrides.
- Advertised model examples: `gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol`, `gpt-6-astra`. These advertise low, medium, high, xhigh, max in this session. No new live model-switching probes were performed.
- Parent settings cannot be inferred from disk defaults. Pilot does not implement Parent switching or Fast/Ultra activation.
- Ponytail 4.9.0 instructions are advertised in this session. Its presence is optional for the shipped policy.

Serena, Context7, Headroom, and Semgrep integrations and versions were **not verified** in this update. They are provider examples only; capability fallbacks and missing-provider behavior are evaluated separately from live integrations.

The package remains skills-only. Source edits do not establish that an installed marketplace cache refreshed; start a new task after the host's update mechanism completes.

Local structural validation and behavioral evaluation results are recorded in [verification](verification.md). Windows, WSL, Linux devices, remote CI, and external-provider compatibility were not exercised in this update. Historical 0.3 host probes remain in Git history and are not claims about 0.4.
