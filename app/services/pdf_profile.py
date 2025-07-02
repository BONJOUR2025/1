"""PDF profile generation service without external dependencies."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from app.data.employee_repository import EmployeeRepository
    from app.data.payout_repository import PayoutRepository
    from app.data.vacation_repository import VacationRepository


def generate_employee_pdf(
    user_id: int,
    employee_repo: "EmployeeRepository",
    payout_repo: "PayoutRepository",
    vacation_repo: "VacationRepository",
) -> bytes:
    """Return a very simple PDF-like document with employee info."""
    employees = employee_repo.list_employees()
    employee = next((e for e in employees if str(e.id) == str(user_id)), None)
    if not employee:
        raise ValueError("Employee not found")

    payouts = payout_repo.list(employee_id=str(user_id))
    vacations = [v for v in vacation_repo.list() if str(v.get("employee_id")) == str(user_id)]

    lines = [
        "👤 PERSONAL DETAILS",
        f"Full name: {getattr(employee, 'full_name', '')}",
        f"Telegram ID: {employee.id}",
        f"Code: {getattr(employee, 'name', '')}",
        "",
        "💸 PAYOUT HISTORY",
    ]
    for p in payouts:
        lines.append(f"{p.get('timestamp', '')} | {p.get('amount')} ₽ | {p.get('status', '')}")
    lines.append("")
    lines.append("📅 VACATION")
    for v in vacations:
        lines.append(f"{v.get('start_date')} → {v.get('end_date')}")
    lines.append("")
    lines.append("📊 STATS")
    status_counts = {}
    for p in payouts:
        status = p.get("status", "")
        status_counts[status] = status_counts.get(status, 0) + 1
    for status, count in status_counts.items():
        lines.append(f"{status}: {count}")
    document = "\n".join(lines)
    # return as bytes so PdfReader stub can decode
    return document.encode("utf-8")
