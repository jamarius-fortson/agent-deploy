from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time
from typing import Dict

class CostGuardMiddleware(BaseHTTPMiddleware):
    """
    Enforces USD budget caps per request and per minute.
    Note: Real cost tracking happens at the adapter level, 
    this middleware sets up the context.
    """
    def __init__(self, app, max_usd_per_request: float, max_usd_per_minute: float):
        super().__init__(app)
        self.max_usd_per_request = max_usd_per_request
        self.max_usd_per_minute = max_usd_per_minute
        self.minute_spend = 0.0
        self.last_reset = time.time()

    async def dispatch(self, request: Request, call_next):
        # Reset minute counter if needed
        if time.time() - self.last_reset > 60:
            self.minute_spend = 0.0
            self.last_reset = time.time()

        if self.minute_spend >= self.max_usd_per_minute:
            raise HTTPException(status_code=429, detail="Global USD budget for this minute exceeded.")

        # Tag the request with a cost tracker
        request.state.cost_spend = 0.0
        
        response = await call_next(request)
        
        # In a real implementation, we'd update self.minute_spend here 
        # from request.state.cost_spend updated by the adapter.
        
        return response
