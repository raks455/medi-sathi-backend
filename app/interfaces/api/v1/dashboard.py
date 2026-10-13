from fastapi import APIRouter, Depends
from app.interfaces.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", summary="Dashboard data for the logged-in user")
async def get_dashboard(current_user=Depends(get_current_user)):
    return {
        "user": {
            "id": str(current_user.id),
            "full_name": current_user.full_name,
            "email": current_user.email,
        },
        "greeting": f"Welcome back, {current_user.full_name}",
        "stats": {},  # fill in once you decide what to show
    }