from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from telegram import Update
from pathlib import Path

from ..config import TOKEN
from ..core.application import create_application
from .employees import create_employee_router
from .salary import create_salary_router
from .schedule import create_schedule_router
from .payouts import create_payout_router
from .birthdays import create_birthdays_router
from .telegram import create_telegram_router
from ..services.employee_service import EmployeeService, EmployeeAPIService
from ..services.salary_service import SalaryService
from ..services.schedule_service import ScheduleService
from ..services.payout_service import PayoutService
from ..services.telegram_service import TelegramService
from ..services.birthday_service import BirthdayService
from ..services.vacation_service import VacationService
from ..services.adjustment_service import AdjustmentService
from ..services.message_service import MessageService
from ..services.analytics import AnalyticsService
from .vacations import create_vacation_router
from .adjustments import create_adjustment_router


def create_app() -> FastAPI:
    app = FastAPI()

    telegram_app = None
    if TOKEN and TOKEN != "dummy":
        telegram_app = create_application()
    # Mount static files for admin UI and React frontend
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/status", response_class=HTMLResponse)
    async def status_page():
        return "<h1>\u0421\u0435\u0440\u0432\u0435\u0440 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442</h1>"

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return Response(status_code=204)

    @app.get("/ping")
    async def ping():
        return {"status": "ok"}

    if telegram_app is not None:
        @app.on_event("startup")
        async def startup():
            await telegram_app.initialize()
            await telegram_app.start()

        @app.on_event("shutdown")
        async def shutdown():
            await telegram_app.stop()
            await telegram_app.shutdown()

    employee_service = EmployeeService()
    employee_api = EmployeeAPIService(employee_service)
    app.include_router(create_employee_router(employee_api), prefix="/api")

    salary_service = SalaryService(employee_service._repo)
    app.include_router(create_salary_router(salary_service), prefix="/api")

    schedule_service = ScheduleService()
    app.include_router(create_schedule_router(schedule_service), prefix="/api")

    telegram_service = TelegramService(employee_service._repo)
    payout_service = PayoutService(telegram_service=telegram_service)
    app.include_router(create_payout_router(payout_service), prefix="/api")

    birthday_service = BirthdayService(employee_service._repo)
    app.include_router(
        create_birthdays_router(birthday_service),
        prefix="/api")

    vacation_service = VacationService()
    app.include_router(create_vacation_router(vacation_service), prefix="/api")

    adjustment_service = AdjustmentService()
    app.include_router(create_adjustment_router(
        adjustment_service), prefix="/api")

    from .messages import create_message_router
    message_service = MessageService(employee_repo=employee_service._repo)
    app.include_router(create_message_router(message_service), prefix="/api")

    from .analytics import create_analytics_router
    analytics_service = AnalyticsService()
    app.include_router(create_analytics_router(analytics_service), prefix="/api")

    app.include_router(
        create_telegram_router(
            employee_service._repo),
        prefix="/api")


    frontend_path = (
        Path(__file__).resolve().parent.parent.parent
        / "admin_frontend"
        / "dist"
    )
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

    if telegram_app is not None:
        @app.post("/webhook")
        async def webhook(request: Request):
            data = await request.json()
            update = Update.de_json(data, telegram_app.bot)
            await telegram_app.process_update(update)
            return {"status": "ok"}

    return app
