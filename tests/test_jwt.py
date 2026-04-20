import jwt
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from fastapixkit import FastAPIXKitConfig, setup_fastapixkit
from fastapixkit.security.jwt import require_jwt_user

def test_jwt_auth():
    app = FastAPI()
    config = FastAPIXKitConfig(jwt_secret="abc")
    setup_fastapixkit(app, config)

    @app.get("/secure")
    def secure(user=Depends(require_jwt_user(config))):
        return {"sub": user["sub"]}

    token = jwt.encode({"sub": "u1", "roles": ["user"]}, "abc", algorithm="HS256")
    client = TestClient(app)
    r = client.get("/secure", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
