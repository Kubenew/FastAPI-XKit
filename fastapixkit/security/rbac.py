from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from .jwt import require_jwt_user
from ..config import FastAPIXKitConfig

def require_role(config: FastAPIXKitConfig, role: str):
    async def _check(user=Depends(require_jwt_user(config))):
        roles = user.get("roles") or []
        if role not in roles:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user
    return _check
