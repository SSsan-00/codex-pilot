from __future__ import annotations

import json
import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "codex-pilot"


class PackageContractTests(unittest.TestCase):
    def test_package(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["version"], "0.4.0")
        self.assertTrue((ROOT / manifest["skills"] / "codex-pilot/SKILL.md").is_file())
        for key in ("hooks", "apps", "mcpServers"):
            self.assertNotIn(key, manifest)
        self.assertIn("allow_implicit_invocation: true", (SKILL / "agents/openai.yaml").read_text())

    def test_corpus_consistency(self):
        corpus = json.loads((ROOT / "evals/cases.json").read_text())
        config = tomllib.loads((ROOT / "examples/codex-pilot.toml").read_text())
        self.assertEqual(config, {"policy": "quality", "max_agents": 2, "show_routing": True})
        self.assertEqual(corpus["defaults"], config)
        self.assertEqual(corpus["schema_version"], 2)
        capabilities = {"semantic_navigation", "current_documentation", "context_compression", "security_analysis"}
        floors = {
            "SIMPLE": ("efficient sufficient capability", "focused"),
            "NORMAL": ("balanced capability", "relevant"),
            "COMPLEX": ("strong capability", "broader"),
            "CRITICAL": ("strongest sufficient available capability", "independent"),
        }
        cases = corpus["decisions"] + corpus["scenarios"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(corpus["decisions"]), 18)
        self.assertEqual(len(corpus["scenarios"]), 21)
        observed = set()
        for case in corpus["decisions"]:
            result = case["expected"]
            self.assertEqual((result["floor"], result["verification"]), floors[result["classification"]])
            self.assertLessEqual(set(result["capabilities"]), capabilities)
            observed.update(result["capabilities"])
            self.assertLessEqual(set(result.get("optional_capabilities", {})), capabilities)
            for alternative in result.get("accepted_alternatives", []):
                self.assertEqual((alternative["floor"], alternative["verification"]), floors[alternative["classification"]])
                self.assertTrue(alternative["condition"])
        self.assertEqual(observed, capabilities)
        for case in corpus["scenarios"]:
            self.assertTrue(case["context"])
            self.assertTrue(case["expected"])

    def test_markdown_links(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            for target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).exists(), f"{path}: {target}")

    def test_removed_runtime_contracts(self):
        runtime = "\n".join(p.read_text() for p in SKILL.rglob("*.md") if p.name != "configuration.md")
        for old_key in ("suggest_parent_upgrade", "suggest_parent_downgrade", "max_escalations", "min_reasoning", "max_reasoning", "allow_fast", "allow_ultra"):
            self.assertNotIn(old_key, runtime)
        self.assertNotRegex(runtime, r"\[(?:Luna|Terra|Sol|Astra)-\d\]")
        self.assertFalse((SKILL / "references/escalation.md").exists())


if __name__ == "__main__":
    unittest.main()
