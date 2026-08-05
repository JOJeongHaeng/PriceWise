from pathlib import Path


def test_demo_checklist_exists():
    assert Path("docs/plans/2026-08-05-local-demo-checklist.md").exists()
