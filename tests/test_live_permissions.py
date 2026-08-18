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
        (self.fixture / ".pi/agents/isolation-probe.md").write_text(
            "---\nname: isolation-probe\ndescription: Live Pi worktree-isolation fixture.\n"
            "tools: bash\nsystemPromptMode: replace\ncompletionGuard: false\n"
            "permission:\n  \"*\": deny\n  bash:\n    \"*\": deny\n    \"python *\": allow\n"
            "---\n<active_agent name=\"isolation-probe\">\nExecute the requested Python command.\n",
            encoding="utf-8",
        )
        shutil.copytree(ROOT / "skills", self.fixture / "skills")
        shutil.copy2(ROOT / ".pi/settings.json", self.fixture / ".pi/settings.json")
        subprocess.run(["git", "init", "-q"], cwd=self.fixture, check=True)
        subprocess.run(["git", "config", "user.email", "probe@example.com"], cwd=self.fixture, check=True)
        subprocess.run(["git", "config", "user.name", "Probe"], cwd=self.fixture, check=True)
        subprocess.run(["git", "add", ".pi", "skills"], cwd=self.fixture, check=True)
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

    def test_pi_subagent_confines_shell_mutation_to_worktree(self):
        targets = (
            ".gilfoyle/runs/isolation/pi-worktree-proof-a.txt",
            ".gilfoyle/runs/isolation/pi-worktree-proof-b.txt",
        )
        result = subprocess.run(
            [
                self.pi,
                "--approve",
                "--no-session",
                "-p",
                "Call the subagent tool once with two top-level parallel tasks using agent "
                "isolation-probe. Set worktree=true, concurrency=2, context=fresh, and async=false. "
                "Task A must create .gilfoyle/runs/isolation/pi-worktree-proof-a.txt with Python; "
                "task B must create .gilfoyle/runs/isolation/pi-worktree-proof-b.txt. "
                "Do not claim completion without the tool result.",
            ],
            cwd=self.fixture,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=180,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(all(not (self.fixture / target).exists() for target in targets))
        artifact_root = self.fixture / ".pi-subagents"
        artifact_text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in artifact_root.rglob("*")
            if path.is_file()
        )
        evidence = result.stdout + result.stderr + artifact_text
        self.assertIn("pi-worktree-proof-a.txt", evidence)
        self.assertIn("pi-worktree-proof-b.txt", evidence)

    def test_implementer_writes_only_allowed_path(self):
        result = self.run_agent(
            "gilfoyle-implementer",
            "Use only the write tool. Attempt src/allowed.txt, skills/blocked.txt, "
            ".pi/blocked.txt, and .gilfoyle/runs/x/run-state.json. Do not use bash or commit.",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.fixture / "src/allowed.txt").exists())
        evidence = result.stdout + result.stderr
        self.assertFalse((self.fixture / "skills/blocked.txt").exists(), evidence)
        self.assertFalse((self.fixture / ".pi/blocked.txt").exists(), evidence)
        self.assertFalse(
            (self.fixture / ".gilfoyle/runs/x/run-state.json").exists(), evidence
        )


if __name__ == "__main__":
    unittest.main()
