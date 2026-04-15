from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/metadata")
async def get_metadata(request: Request):
    agent = request.app.state.agent
    return agent.get_metadata()
