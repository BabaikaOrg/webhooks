from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def status():
    """Health check endpoint"""
    return {"message": "Smooth ride"}
