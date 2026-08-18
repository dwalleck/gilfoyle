import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = ROOT / ".pi/settings.json"
EXPECTED_PACKAGES = [
    "npm:pi-subagents@0.34.0",
    "npm:@gotgenes/pi-permission-system@20.3.0",
]
EXPECTED_SKILLS = {"gilfoyle"}
EXPECTED_COMPONENTS = {"skills": 1, "agents": 5, "chains": 2}
EXPECTED_PLUGIN_VERSION = "2.0.1"
KIRO_SKILL_URI = "skill://.kiro/skills/gilfoyle/SKILL.md"
KIRO_FILE_PREFIX = "file://../skills/gilfoyle/"


class ConfigurationTests(unittest.TestCase):
    def test_project_settings_resolve_unified_skills(self):
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        configured = (SETTINGS.parent / settings["skills"][0]).resolve()
        legacy = ROOT / "pi-skills"
        self.assertEqual(ROOT / "skills", configured)
        self.assertFalse(legacy.exists())
        self.assertTrue((ROOT / "skills/gilfoyle/SKILL.md").is_file())

    def test_project_packages_are_pinned_to_probed_versions(self):
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        self.assertEqual(EXPECTED_PACKAGES, settings["packages"])

    def test_exact_skill_manifest(self):
        skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
        names = set()
        for skill_file in skill_files:
            name_line = next(
                line
                for line in skill_file.read_text(encoding="utf-8").splitlines()
                if line.startswith("name:")
            )
            names.add(name_line.partition(":")[2].strip())
        self.assertEqual(EXPECTED_SKILLS, names)
        self.assertEqual(len(EXPECTED_SKILLS), len(skill_files))

    def test_plugin_manifests_share_version_and_skill_root(self):
        portable = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        claude = json.loads(
            (ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        versions = {
            portable["version"],
            package["version"],
            claude["version"],
            marketplace["plugins"][0]["version"],
        }
        self.assertEqual({EXPECTED_PLUGIN_VERSION}, versions)
        self.assertNotIn("skills", claude)

    def test_kiro_resources_resolve_unified_skill(self):
        source_root = ROOT / "skills/gilfoyle"
        for config_path in sorted((ROOT / "agents").glob("gilfoyle-*.json")):
            resources = json.loads(config_path.read_text(encoding="utf-8"))["resources"]
            self.assertEqual(KIRO_SKILL_URI, resources[0], config_path)
            for resource in resources[1:]:
                self.assertTrue(resource.startswith(KIRO_FILE_PREFIX), config_path)
                source = source_root / resource.removeprefix(KIRO_FILE_PREFIX)
                self.assertTrue(source.is_file(), source)

    def test_expected_manifest_is_bounded(self):
        self.assertEqual(len(EXPECTED_SKILLS), EXPECTED_COMPONENTS["skills"])
        self.assertEqual(8, sum(EXPECTED_COMPONENTS.values()))


if __name__ == "__main__":
    unittest.main()
