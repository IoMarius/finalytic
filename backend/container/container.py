from dependency_injector import containers, providers
from data import get_session
from data.repositories import ExpensesRepository, UserRepository, ReceiptRepository
from jobs import UsersExpensesJob


class Container(containers.DeclarativeContainer):
    session_factory = providers.Factory(get_session)

    user_repo = providers.Factory(UserRepository, session=session_factory)

    receipt_repo = providers.Factory(ReceiptRepository, session=session_factory)

    expenses_repo = providers.Factory(ExpensesRepository, session=session_factory)

    users_expenses_job = providers.Factory(
        UsersExpensesJob,
        user_repo=user_repo,
        receipt_repo=receipt_repo,
        expenses_repo=expenses_repo,
    )

di = Container()

# Use:
# container = Container()
# async with container.session_factory() as session:
#     job = container.users_expenses_job()
#     await job.for_all_users(period)
