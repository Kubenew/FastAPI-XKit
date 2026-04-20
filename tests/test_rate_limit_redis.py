from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapixkit import FastAPIXKitConfig, setup_fastapixkit

def test_rate_limit_wiring():
    app = FastAPI()
    config = FastAPIXKitConfig(rate_limit_per_minute=999999)
    setup_fastapixkit(app, config)
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
