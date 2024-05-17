from typing import Optional
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from fastapi import Request

from jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "sebastian.sarasti@tupana.com":
            raise HTMLResponse(status_code=403, content="Unauthorized")