import jwt
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from fastapixkit import FastAPIXKitConfig, setup_fastapixkit
from fastapixkit.security.rbac import require_role

def test_rbac_admin():
    app = FastAPI()
    config = FastAPIXKitConfig(jwt_secret="abc")
    setup_fastapixkit(app, config)

    @app.get("/admin")
    def admin(user=Depends(require_role(config, "admin"))):
        return {"ok": True}

    token_user = jwt.encode({"sub": "u1", "roles": ["user"]}, "abc", algorithm="HS256")
    token_admin = jwt.encode({"sub": "u2", "roles": ["admin"]}, "abc", algorithm="HS256")

    client = TestClient(app)

    r1 = client.get("/admin", headers={"Authorization": f"Bearer {token_user}"})
    assert r1.status_code == 403

    r2 = client.get("/admin", headers={"Authorization": f"Bearer {token_admin}"})
    assert r2.status_code == 200
