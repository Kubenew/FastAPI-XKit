from typing import Dict, Any
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from ..config import FastAPIXKitConfig

_bearer = HTTPBearer(auto_error=False)

def decode_jwt(token: str, config: FastAPIXKitConfig) -> Dict[str, Any]:
    return jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])

def require_jwt_user(config: FastAPIXKitConfig):
    async def _auth(creds: HTTPAuthorizationCredentials = Security(_bearer)):
        if not creds:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")
        try:
            payload = decode_jwt(creds.credentials, config)
        except Exception:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid JWT")
        return payload
    return _auth
