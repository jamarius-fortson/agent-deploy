from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
async def healthz():
    return {"status": "ok"}

@router.get("/readyz")
async def readyz():
    # TODO: Check LLM provider reachability via adapter
    return {"status": "ready"}
