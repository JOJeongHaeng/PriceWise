from main import app_entrypoints


def test_app_entrypoints_exposes_pipeline_and_dashboard():
    entrypoints = app_entrypoints()
    assert "pipeline" in entrypoints
    assert "dashboard" in entrypoints
