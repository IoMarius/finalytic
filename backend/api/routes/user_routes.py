from fastapi import APIRouter
from models.receipt import APIResponse
from jobs import run_user_expenses
from data import CalculationPeriod

user_router = APIRouter(prefix="/api/v1/users")


@user_router.get("")
async def store_as_json() -> APIResponse:
    return APIResponse(
        success=True,
        message="Well hello there :)",
    )


@user_router.get("jababi")
async def popka() -> APIResponse:
    await run_user_expenses(calculation_period=CalculationPeriod.YEAR)
    return APIResponse(
        success=True,
        message="Well hello there :)",
    )
