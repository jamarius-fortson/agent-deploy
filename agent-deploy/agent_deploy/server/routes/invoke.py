from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any

router = APIRouter()

@router.post("/invoke")
async def invoke(request: Request, input_data: Dict[str, Any]):
    agent = request.app.state.agent
    try:
        result = await agent.invoke(input_data)
        return {"result": result}
    except Exception as e:
        # TODO: Better error handling with structured logs
        raise HTTPException(status_code=500, detail=str(e))
