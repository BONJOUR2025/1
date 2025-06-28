"""Compatibility wrapper using EmployeeService."""
from typing import Dict, Any, List
from .employee_service import EmployeeService
from app.core.types import Employee

_service = EmployeeService()


def load_users_map() -> Dict[str, Any]:
    return {e.id: {
        "name": e.name,
        "full_name": e.full_name,
        "phone": e.phone,
        "position": e.position,
        "is_admin": e.is_admin,
        "card_number": e.card_number,
        "bank": e.bank,
        "birthdate": e.birthdate.isoformat() if e.birthdate else None,
        "note": e.note,
        "photo_url": e.photo_url,
        "status": e.status.value,
    } for e in _service.list_employees()}


def save_users(users: Dict[str, Any]) -> None:
    objs = []
    for uid, data in users.items():
        objs.append(Employee(
            id=str(uid),
            name=data.get("name", ""),
            full_name=data.get("full_name", ""),
            phone=data.get("phone", ""),
            position=data.get("position", ""),
            is_admin=data.get("is_admin", False),
            card_number=data.get("card_number", ""),
            bank=data.get("bank", ""),
            birthdate=data.get("birthdate"),
            note=data.get("note", ""),
            photo_url=data.get("photo_url", ""),
            status=data.get("status", "active"),
        ))
    _service._repo.save_employees(objs)

