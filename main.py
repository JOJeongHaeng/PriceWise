def app_entrypoints() -> dict[str, str]:
    return {
        "pipeline": "etl.jobs.run_pipeline:run_pipeline",
        "dashboard": "app.dashboard.home",
    }
