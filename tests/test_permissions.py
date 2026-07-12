import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".pi/agents"
EXPECTED = {
    "gilfoyle-prober",
    "gilfoyle-designer",
    "gilfoyle-planner",
    "gilfoyle-implementer",
    "gilfoyle-gatekeeper",
}
PROTECTED = (
    ".pi/*",
    "pi-skills/*",
    "skills/*",
    "agents/*",
    "crew-dag-loop.json",
    ".gilfoyle/runs/*",
)


def agent_fields(path):
    text = path.read_text(encoding="utf-8")
    name_match = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
    tools_match = re.search(r"^tools:\s*(.+)$", text, re.MULTILINE)
    if name_match is None or tools_match is None:
        raise AssertionError(f"missing agent frontmatter in {path}")
    name = name_match.group(1).strip()
    tools = tools_match.group(1).split(",")
    return text, name, {tool.strip() for tool in tools}


class PermissionContractTests(unittest.TestCase):
    def test_exact_leaf_set_and_matching_markers(self):
        parsed = [agent_fields(path) for path in sorted(AGENTS.glob("*.md"))]
        self.assertEqual(EXPECTED, {name for _, name, _ in parsed})
        self.assertEqual(len(EXPECTED), len(parsed))
        for text, name, tools in parsed:
            self.assertIn(f'<active_agent name="{name}">', text)
            self.assertNotIn("subagent", tools)
            self.assertIn("defaultContext: fresh", text)

    def test_only_implementer_has_mutation_tools(self):
        for path in AGENTS.glob("*.md"):
            _, name, tools = agent_fields(path)
            if name == "gilfoyle-implementer":
                self.assertTrue({"write", "edit"} <= tools)
            else:
                self.assertTrue({"write", "edit"}.isdisjoint(tools))

    def test_implementer_denies_control_plane_paths(self):
        text, _, _ = agent_fields(AGENTS / "gilfoyle-implementer.md")
        for pattern in PROTECTED:
            self.assertGreaterEqual(text.count(f'"{pattern}": deny'), 2)
        self.assertNotIn('"git push *": allow', text)
        self.assertNotIn('"git reset *": allow', text)
        self.assertNotIn('"git clean *": allow', text)


if __name__ == "__main__":
    unittest.main()
