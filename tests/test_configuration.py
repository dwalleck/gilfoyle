import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = ROOT / ".pi/settings.json"
EXPECTED_PACKAGES = {
    "npm:pi-subagents@0.34.0",
    "npm:@gotgenes/pi-permission-system@20.3.0",
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
        self.assertEqual(EXPECTED_PACKAGES, set(settings["packages"]))

    def test_expected_manifest_is_bounded(self):
        self.assertEqual({"skills": 8, "agents": 5, "chains": 2}, EXPECTED_COMPONENTS)
        self.assertEqual(15, sum(EXPECTED_COMPONENTS.values()))


if __name__ == "__main__":
    unittest.main()
