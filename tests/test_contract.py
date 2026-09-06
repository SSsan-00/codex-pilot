from __future__ import annotations

import json
import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "codex-pilot"


class PackageContractTests(unittest.TestCase):
    def test_plugin_manifest_points_to_real_skill_tree(self) -> None:
        manifest = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["name"], "codex-pilot")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertNotIn("apps", manifest)
        self.assertNotIn("mcpServers", manifest)
        self.assertNotIn("hooks", manifest)

    def test_skill_identity_and_implicit_policy(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---\n", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: codex-pilot$")
        self.assertRegex(frontmatter, r"(?m)^description: .+software-development.+$")

        agent_config = (SKILL_ROOT / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("allow_implicit_invocation: true", agent_config)
        self.assertIn("$codex-pilot", agent_config)

    def test_default_configuration_matches_public_contract(self) -> None:
        config = tomllib.loads(
            (ROOT / "examples" / "codex-pilot.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            config,
            {
                "policy": "quality",
                "allow_fast": False,
                "allow_ultra": True,
                "min_reasoning": "medium",
                "max_reasoning": "max",
                "max_escalations": 2,
                "max_agents": 3,
                "ponytail": "required",
                "show_routing": True,
                "suggest_parent_upgrade": True,
                "suggest_parent_downgrade": True,
            },
        )

    def test_evaluation_corpus_covers_required_cases(self) -> None:
        corpus = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(corpus["routing"]), 7)
        self.assertEqual(len(corpus["parent_upgrade"]), 4)
        self.assertEqual(len(corpus["escalation"]), 5)
        self.assertEqual(len(corpus["ponytail_integration"]), 8)
        self.assertTrue(corpus["escalation_cases_are_independent"])
        self.assertTrue(corpus["default_budget_does_not_traverse_full_ladder"])

        visibility = corpus["routing_visibility"]
        self.assertTrue(visibility["default_show_routing"])
        self.assertTrue(visibility["normal_completion"]["final_response_line"])
        self.assertTrue(
            visibility["normal_completion"]["family_relative_strength_label"]
        )
        self.assertTrue(
            visibility["normal_completion"]["strength_is_not_cross_family_rank"]
        )
        self.assertFalse(
            visibility["normal_completion"]["commentary_only_sufficient"]
        )
        self.assertTrue(visibility["normal_completion"]["exactly_one_line"])
        self.assertTrue(visibility["normal_completion"]["standalone_final_line"])
        self.assertTrue(
            visibility["normal_completion"]["missing_line_means_incomplete"]
        )
        self.assertTrue(all(visibility["normal_completion"]["workers"].values()))

        ids = [
            case["id"]
            for group in (
                "routing",
                "parent_upgrade",
                "escalation",
                "ponytail_integration",
            )
            for case in corpus[group]
        ]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(corpus["route_only"]["must_not_modify_files"])
        self.assertTrue(corpus["route_only"]["must_not_run_mutating_commands"])
        self.assertTrue(corpus["route_only"]["must_not_spawn_agents"])
        self.assertTrue(corpus["route_only"]["must_not_solve_or_reproduce_clear_task"])
        self.assertEqual(
            corpus["family_relative_strength"],
            {"low": 1, "medium": 2, "high": 3, "xhigh": 4, "max": 5},
        )

        concurrency = next(
            case
            for case in corpus["routing"]
            if case["id"] == "route-05-concurrency"
        )
        self.assertEqual(concurrency["expected"]["ultra_candidate"], "conditional")
        self.assertTrue(
            concurrency["expected"]["ultra_conditions"][
                "host_and_account_expose_ultra"
            ]
        )
        ambiguous = next(
            case
            for case in corpus["routing"]
            if case["id"] == "route-07-small-ambiguous"
        )
        self.assertTrue(ambiguous["expected"]["luna_forbidden"])
        critical = next(
            case
            for case in corpus["routing"]
            if case["id"] == "route-04-large-migration"
        )
        self.assertEqual(critical["expected"]["family"], "Astra")
        self.assertEqual(critical["expected"]["strength_label"], "Astra-5")

        parent = {case["id"]: case for case in corpus["parent_upgrade"]}
        self.assertFalse(parent["parent-c"]["expected"]["downgrade_visible"])
        self.assertTrue(
            parent["parent-d"]["expected"]["default_downgrade_visible"]
        )
        self.assertTrue(parent["parent-d"]["expected"]["must_not_interrupt"])

        ponytail = {case["id"]: case for case in corpus["ponytail_integration"]}
        self.assertTrue(
            ponytail["ponytail-default-required-absent"]["expected"][
                "stop_before_implementation"
            ]
        )
        self.assertTrue(
            ponytail["ponytail-default-required-absent"]["expected"][
                "report_missing_dependency"
            ]
        )
        self.assertTrue(
            ponytail["ponytail-pilot-only-invocation"]["expected"][
                "invoke_ponytail"
            ]
        )
        self.assertFalse(
            ponytail["ponytail-pilot-only-invocation"]["expected"][
                "require_separate_user_invocation"
            ]
        )
        self.assertFalse(
            ponytail["ponytail-ultra-is-not-codex-ultra"]["expected"][
                "codex_ultra_activated"
            ]
        )
        self.assertFalse(
            ponytail["ponytail-route-only"]["expected"]["invoke_ponytail"]
        )
        self.assertTrue(
            ponytail["ponytail-preserves-scope"]["expected"][
                "preserve_user_acceptance_criteria"
            ]
        )

    def test_references_resolve_and_are_progressively_routed(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\((references/[^)]+)\)", skill)
        self.assertGreaterEqual(len(set(links)), 4)
        for relative in set(links):
            self.assertTrue((SKILL_ROOT / relative).is_file(), relative)

    def test_all_relative_markdown_links_resolve(self) -> None:
        for document in ROOT.rglob("*.md"):
            if ".git" in document.parts:
                continue
            contents = document.read_text(encoding="utf-8")
            for raw_target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", contents):
                if "://" in raw_target or raw_target.startswith(("#", "mailto:")):
                    continue
                target = raw_target.split("#", 1)[0]
                self.assertTrue(
                    (document.parent / target).resolve().exists(),
                    f"{document.relative_to(ROOT)} -> {raw_target}",
                )

    def test_no_personal_absolute_paths_or_secret_placeholders(self) -> None:
        checked_suffixes = {".md", ".json", ".toml", ".yaml", ".yml", ".py"}
        posix_home_prefix = "/" + "Users" + "/"
        windows_home_pattern = r"(?i)[A-Z]:\\" + "Users" + r"\\[^<]"
        todo_marker = "[" + "TODO:"
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path.suffix not in checked_suffixes:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(posix_home_prefix, text, str(path))
            self.assertNotRegex(text, windows_home_pattern, str(path))
            self.assertNotIn(todo_marker, text, str(path))
            self.assertNotRegex(text, r"sk-[A-Za-z0-9]{16,}", str(path))


if __name__ == "__main__":
    unittest.main()
