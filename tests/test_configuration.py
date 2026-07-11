import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = ROOT / ".pi/settings.json"
EXPECTED_PACKAGES = [
    "npm:pi-subagents@0.34.0",
    "npm:@gotgenes/pi-permission-system@20.3.0",
]
EXPECTED_SKILLS = {
    "assessing-review-feedback",
    "budgeted-plan",
    "checkpointed-build",
    "falsifiable-design",
    "gilfoyle-workflow",
    "interrogated-spec",
    "prove-it-prototype",
    "tdd-scoped",
}
EXPECTED_COMPONENTS = {"skills": 8, "agents": 5, "chains": 2}


class ConfigurationTests(unittest.TestCase):
    def test_project_settings_resolve_pi_skills(self):
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        configured = (SETTINGS.parent / settings["skills"][0]).resolve()
        buggy = (SETTINGS.parent / "pi-skills").resolve()
        self.assertEqual(ROOT / "pi-skills", configured)
        self.assertNotEqual(configured, buggy)
        self.assertFalse(buggy.exists())

    def test_project_packages_are_pinned_to_probed_versions(self):
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        self.assertEqual(EXPECTED_PACKAGES, settings["packages"])

    def test_exact_pi_skill_manifest(self):
        skill_files = sorted((ROOT / "pi-skills").glob("*/SKILL.md"))
        names = set()
        for skill_file in skill_files:
            name_line = next(
                line for line in skill_file.read_text(encoding="utf-8").splitlines()
                if line.startswith("name:")
            )
            names.add(name_line.partition(":")[2].strip())
        self.assertEqual(EXPECTED_SKILLS, names)
        self.assertEqual(len(EXPECTED_SKILLS), len(skill_files))

    def test_expected_manifest_is_bounded(self):
        self.assertEqual(len(EXPECTED_SKILLS), EXPECTED_COMPONENTS["skills"])
        self.assertEqual(15, sum(EXPECTED_COMPONENTS.values()))


if __name__ == "__main__":
    unittest.main()
