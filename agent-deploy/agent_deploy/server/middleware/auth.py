import os
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Optional

class BearerAuthMiddleware(BaseHTTPMiddleware):
    """
    Simple Bearer Token authentication.
    Reads valid keys from an environment variable.
    """
    def __init__(self, app, env_var: str = "ADEPLOY_API_KEYS"):
        super().__init__(app)
        self.env_var = env_var
        self.valid_keys = self._load_keys()

    def _load_keys(self) -> List[str]:
        keys_str = os.getenv(self.env_var, "")
        if not keys_str:
            return []
        return [k.strip() for k in keys_str.split(",") if k.strip()]

    async def dispatch(self, request: Request, call_next):
        # Skip auth for health checks
        if request.url.path in ["/healthz", "/readyz"]:
            return await call_next(request)

        if not self.valid_keys:
            # If no keys are configured, we allow all in dev, or block all in prod.
            # Here we default to blocking for safety.
            raise HTTPException(status_code=401, detail="No API keys configured on server.")

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")

        token = auth_header.split(" ")[1]
        if token not in self.valid_keys:
            raise HTTPException(status_code=403, detail="Invalid API key.")

        return await call_next(request)
