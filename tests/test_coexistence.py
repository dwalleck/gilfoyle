import hashlib
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = (ROOT / "skills", ROOT / "agents", ROOT / "crew-dag-loop.json")
EXPECTED_DIGEST = "86a8c6eb7b2467c9b8fde65b5a6f846df3f64387513108f07a93e00b460fc4b4"
IGNORED = (
    ".gilfoyle/runs/naïve path/run-state.json",
    ".pi-native-workflow/probe.tmp",
    "skills/interrogated-spec-workspace/case.tmp",
    ".pi-subagents/runtime.tmp",
    "tests/__pycache__/case.pyc",
)


def protected_digest():
    files = []
    for root in PROTECTED:
        files.extend([root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()])
    files = [p for p in files if ".pi-subagents" not in p.parts and "interrogated-spec-workspace" not in p.parts]
    digest = hashlib.sha256()
    for path in sorted(files):
        digest.update(path.relative_to(ROOT).as_posix().encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


class CoexistenceTests(unittest.TestCase):
    def test_kiro_baseline(self):
        self.assertEqual(EXPECTED_DIGEST, protected_digest())

    def test_runtime_artifacts_are_ignored_but_other_files_are_not(self):
        paths = [*IGNORED, "outside-run.tmp"]
        try:
            for relative in paths:
                path = ROOT / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            results = {
                relative: subprocess.run(
                    ["git", "check-ignore", "-q", relative], cwd=ROOT, check=False,
                ).returncode
                for relative in paths
            }
            self.assertTrue(all(results[path] == 0 for path in IGNORED))
            self.assertEqual(1, results["outside-run.tmp"])
        finally:
            for relative in paths:
                (ROOT / relative).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
