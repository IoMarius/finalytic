from fastapi import APIRouter
from models.receipt import APIResponse


user_router = APIRouter(prefix="/api/v1/users")


@user_router.get("")
async def store_as_json() -> APIResponse:

    return APIResponse(
        success=True,
        message="Well hello there :)",
    )
