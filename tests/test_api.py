import shutil
from pathlib import Path
from fastapi.testclient import TestClient
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from main import app, STORAGE_DIR

client = TestClient(app)


def setup_module(module):
    """Prepare a clean test storage directory before all tests."""
    if STORAGE_DIR.exists():
        shutil.rmtree(STORAGE_DIR)
    STORAGE_DIR.mkdir()


def teardown_module(module):
    """Cleanup after all tests."""
    if STORAGE_DIR.exists():
        shutil.rmtree(STORAGE_DIR)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "File Storage API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "File Storage API"


def test_upload_file():
    file_content = b"hello test"
    files = {"file": ("test.txt", file_content, "text/plain")}

    response = client.post("/files", files=files)
    assert response.status_code == 200

    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["size"] == len(file_content)

    # file should exist in storage
    assert (STORAGE_DIR / "test.txt").exists()


def test_get_file():
    # file must already exist from previous test
    response = client.get("/files/test.txt")
    assert response.status_code == 200
    assert response.content == b"hello test"


def test_list_files():
    response = client.get("/files")
    assert response.status_code == 200

    data = response.json()
    assert "files" in data
    assert "test.txt" in data["files"]
    assert data["count"] == 1


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()

    assert "files_current" in data
    assert data["files_current"] >= 1
    assert "total_storage_bytes" in data
