from pathlib import Path


def test_required_project_files_exist():
    required = [
        "README.md",
        ".env.example",
        "requirements.txt",
        "docker-compose.yml",
        "app/dashboard/__init__.py",
        "etl/extract/__init__.py",
        "tests/__init__.py",
    ]
    for path in required:
        assert Path(path).exists(), path
