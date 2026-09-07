import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED = (
    ".gilfoyle/runs/naïve path/run-state.json",
    ".pi-native-workflow/probe.tmp",
    ".pi-subagents/runtime.tmp",
    "tests/__pycache__/case.pyc",
)



class CoexistenceTests(unittest.TestCase):
    def test_runtime_artifacts_are_ignored_but_other_files_are_not(self):
        paths = [*IGNORED, "outside-run.tmp"]
        results = {
            relative: subprocess.run(
                ["git", "check-ignore", "-q", "--no-index", relative],
                cwd=ROOT,
                check=False,
            ).returncode
            for relative in paths
        }
        self.assertTrue(all(results[path] == 0 for path in IGNORED))
        self.assertEqual(1, results["outside-run.tmp"])
        self.assertTrue(all(not (ROOT / relative).exists() for relative in paths))


if __name__ == "__main__":
    unittest.main()
