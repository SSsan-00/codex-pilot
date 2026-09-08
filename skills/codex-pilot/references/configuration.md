# Optional settings

Most tasks need no configuration. Resolve each supported key from current user instructions, then repository `.codex-pilot.toml`, then `$CODEX_HOME/codex-pilot.toml` (normally the user's `.codex` directory), then defaults. Read only these known paths when available; do not scan for configuration or confuse them with the host's `config.toml`.

```toml
policy = "quality"
max_agents = 2
show_routing = true
```

- `policy`: quality, balanced, or throughput; all preserve the reliable floor described in [routing](routing.md).
- `max_agents`: integer 0–8, bounded by host capacity; maximum total Pilot-managed workers per task including retries. Default 2; zero forbids explicit delegation. It does not configure host-internal fan-out.
- `show_routing`: boolean, default true; controls the final Routing line, not a requested route-only summary.

Invalid supported values fall back to defaults. For an unreadable or malformed file, continue with other available settings and briefly report if requested limits could not be resolved. Never create or edit configuration without a user request.

## Migration from 0.3

Only the three keys above remain supported. Legacy `allow_fast`, `allow_ultra`, `min_reasoning`, `max_reasoning`, `max_escalations`, `ponytail`, `suggest_parent_upgrade`, and `suggest_parent_downgrade` keys are ignored. Other unknown keys are ignored too. If a loaded file contains legacy resource limits, briefly disclose that they no longer apply; users should move constraints into explicit task instructions or host settings before relying on them. Explicit current user limits always remain authoritative.

Ponytail is optional, Parent recommendations and custom strength labels are removed, and a meaningful unresolved failure permits at most one justified stronger retry. The worker default changes from three to two. See the [user guide](../../../docs/user-guide.ja.md).
