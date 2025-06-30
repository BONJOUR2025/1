from types import SimpleNamespace
from datetime import date
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app.services.birthday_service as bs
from app.core.enums import EmployeeStatus


class FakeDate(date):
    @classmethod
    def today(cls):
        return FAKE_TODAY


class DummyRepo:
    def list_employees(self):
        return [
            SimpleNamespace(
                id="1",
                full_name="A",
                name="A",
                phone="1",
                birthdate=FakeDate(1990, 12, 31),
                status=EmployeeStatus.ACTIVE,
            ),
            SimpleNamespace(
                id="2",
                full_name="B",
                name="B",
                phone="2",
                birthdate=FakeDate(1990, 1, 1),
                status=EmployeeStatus.ACTIVE,
            ),
            SimpleNamespace(
                id="3",
                full_name="C",
                name="C",
                phone="3",
                birthdate=None,
                status=EmployeeStatus.ACTIVE,
            ),
            SimpleNamespace(
                id="4",
                full_name="D",
                name="D",
                phone="4",
                birthdate=FakeDate(1899, 12, 30),
                status=EmployeeStatus.ACTIVE,
            ),
            SimpleNamespace(
                id="5",
                full_name="E",
                name="E",
                phone="5",
                birthdate=FakeDate(1990, 12, 31),
                status=EmployeeStatus.INACTIVE,
            ),
        ]


FAKE_TODAY = date(2025, 12, 30)


def test_get_upcoming_birthdays(monkeypatch):
    monkeypatch.setattr(bs, "_repo", DummyRepo())
    monkeypatch.setattr(bs, "date", FakeDate)
    res = bs.get_upcoming_birthdays(2)
    assert [r["user_id"] for r in res] == ["1", "2"]
