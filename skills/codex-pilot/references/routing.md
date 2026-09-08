# Execution policy

Select the highest class justified by the task's real consequences and uncertainty, not prompt length or file count.

| Class | Signals | Capability floor | Verification |
| --- | --- | --- | --- |
| SIMPLE | Clear, local, low risk, low uncertainty, easy to verify | efficient sufficient capability | focused check |
| NORMAL | Routine feature, understood bug, test, small/medium refactor | balanced capability | focused tests and relevant checks |
| COMPLEX | Unresolved cause, multi-module flow, DB/cache/async interaction, substantial refactor, multiple hypotheses, difficult verification | strong capability | broader verification where justified |
| CRITICAL | Architecture, security boundary, data integrity, destructive migration, difficult concurrency, distributed systems, large blast radius | strongest sufficient available capability | independent verification of critical assumptions |

Authentication, authorization, security boundaries, data integrity, destructive operations, migrations, concurrency, and externally irreversible actions impose risk floors even for tiny diffs. Boundary-changing or destructive work is CRITICAL; a harmless label near such code is not automatically critical.

Unknown root causes, unfamiliar subsystems, ambiguous requirements, contradictory evidence, or unsettled scope exclude SIMPLE. High uncertainty must not use an efficient-only route. Inspect safely to resolve uncertainty; do not downgrade because the eventual implementation looks short.

## Select sufficient execution

Map the floor to currently advertised model and reasoning capabilities within explicit user limits. No fixed family ladder or private benchmark rank is needed. If the environment cannot meet the floor, say so. Never invent identifiers, silently ignore limits, or describe a recommendation as an applied model switch.

Quality defaults to reliability under remaining uncertainty. Balanced avoids extra computation once the same reliable floor is met. Throughput favors cohesive execution and fewer tool calls while meeting that same floor. No policy weakens necessary verification.

## Verify once, deepen for evidence

Prefer project-native build/compile, focused tests, integration checks at changed boundaries, lint, type checks, and existing static analysis as relevant. Review the actual diff and acceptance criteria. Do not add tests that merely mirror reversible implementation details.

For critical work, independently check security, rollback/data preservation, or concurrency assumptions as applicable; a distinct check or evidence source can suffice without another agent. Preserve original failure evidence. Do not repeat a passed heavy suite without new changes, failures, or unresolved concerns. One stronger bounded retry for a meaningful unresolved failure is defined in the Skill, not a sequence of model promotions. A failed, waived, or unavailable check is never silently treated as passed: apply the Skill’s completion-integrity gate and report partial or blocked status when it prevents completion.
