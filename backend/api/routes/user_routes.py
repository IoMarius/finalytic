from fastapi import APIRouter
from models.receipt import APIResponse

from jobs import UsersExpensesJob
from data.repositories import ExpensesRepository, ReceiptRepository, UserRepository
from data import CalculationPeriod

user_router = APIRouter(prefix="/api/v1/users")


@user_router.get("")
async def store_as_json() -> APIResponse:
    return APIResponse(
        success=True,
        message="Well hello there :)",
    )


@user_router.post("test-job")
async def test() -> APIResponse:
    job = UsersExpensesJob(UserRepository, ReceiptRepository, ExpensesRepository)
    await job.for_all_users(CalculationPeriod.WEEK)
    return APIResponse(
        success=True,
        message="Well hello there :)",
    )
