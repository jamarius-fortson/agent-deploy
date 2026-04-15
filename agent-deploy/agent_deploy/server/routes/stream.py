from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from typing import Dict, Any
import json

router = APIRouter()

@router.post("/stream")
async def stream(request: Request, input_data: Dict[str, Any]):
    agent = request.app.state.agent

    async def event_publisher():
        try:
            async for event in agent.stream(input_data):
                # SSE event format
                yield {
                    "event": event.event_type,
                    "data": json.dumps(event.data) if not isinstance(event.data, str) else event.data
                }
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"detail": str(e)})
            }

    return EventSourceResponse(event_publisher())
