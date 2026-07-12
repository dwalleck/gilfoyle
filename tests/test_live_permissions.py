import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = os.environ.get("GILFOYLE_LIVE_PI") == "1"
NON_WRITERS = (
    "gilfoyle-prober",
    "gilfoyle-designer",
    "gilfoyle-planner",
    "gilfoyle-gatekeeper",
)


@unittest.skipUnless(LIVE, "set GILFOYLE_LIVE_PI=1 for installed-runtime probes")
class LivePermissionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = Path(tempfile.mkdtemp(prefix="gilfoyle-live-permissions-"))
        shutil.copytree(ROOT / ".pi/agents", self.fixture / ".pi/agents")
        shutil.copytree(ROOT / "pi-skills", self.fixture / "pi-skills")
        (self.fixture / ".pi/settings.json").write_text(
            json.dumps({"skills": ["../pi-skills"]}), encoding="utf-8"
        )
        subprocess.run(["git", "init", "-q"], cwd=self.fixture, check=True)
        subprocess.run(["git", "config", "user.email", "probe@example.com"], cwd=self.fixture, check=True)
        subprocess.run(["git", "config", "user.name", "Probe"], cwd=self.fixture, check=True)
        subprocess.run(["git", "add", ".pi", "pi-skills"], cwd=self.fixture, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.fixture, check=True)
        pi = shutil.which("pi.cmd") or shutil.which("pi")
        if pi is None:
            raise RuntimeError("pi executable not found")
        self.pi: str = pi
        self.env = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("PI_SUBAGENT_")
        }

    def tearDown(self):
        shutil.rmtree(self.fixture, ignore_errors=True)

    def run_agent(self, agent, task, cwd=None):
        command = f'/run {agent} "{task}"'
        return subprocess.run(
            [self.pi, "--approve", "--no-session", "-p", command],
            cwd=cwd or self.fixture,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=180,
        )

    def test_non_writers_cannot_create_files(self):
        for agent in NON_WRITERS:
            target = f"forbidden-{agent}.txt"
            result = self.run_agent(
                agent,
                f"Attempt to use the write tool to create {target}. Do not use bash.",
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse((self.fixture / target).exists(), agent)

    def test_shell_mutation_is_confined_to_worktree(self):
        worktree = self.fixture.parent / f"{self.fixture.name}-isolation"
        subprocess.run(
            ["git", "worktree", "add", "-q", "--detach", str(worktree), "HEAD"],
            cwd=self.fixture,
            check=True,
        )
        target = ".gilfoyle/runs/isolation/shell-proof.txt"
        try:
            script = (
                "from pathlib import Path; "
                f"p=Path({target!r}); p.parent.mkdir(parents=True); p.write_text('probe')"
            )
            result = subprocess.run(
                [shutil.which("python") or "python", "-c", script],
                cwd=worktree,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((worktree / target).exists())
            self.assertFalse((self.fixture / target).exists())
        finally:
            subprocess.run(
                ["git", "worktree", "remove", "-f", str(worktree)],
                cwd=self.fixture,
                check=False,
            )

    def test_implementer_writes_only_allowed_path(self):
        result = self.run_agent(
            "gilfoyle-implementer",
            "Use only the write tool. Attempt src/allowed.txt, skills/blocked.txt, "
            ".pi/blocked.txt, and .gilfoyle/runs/x/run-state.json. Do not use bash or commit.",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.fixture / "src/allowed.txt").exists())
        self.assertFalse((self.fixture / "skills/blocked.txt").exists())
        self.assertFalse((self.fixture / ".pi/blocked.txt").exists())
        self.assertFalse((self.fixture / ".gilfoyle/runs/x/run-state.json").exists())


if __name__ == "__main__":
    unittest.main()
