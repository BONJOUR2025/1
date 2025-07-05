import types
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app.services.advance_requests as ar

class DummyRepo:
    def __init__(self):
        self.data = []
        self.counter = 0
    def list(self, employee_id=None, *args, **kwargs):
        if employee_id is None:
            return list(self.data)
        return [d for d in self.data if str(d["user_id"]) == str(employee_id)]
    def load_all(self):
        return list(self.data)
    def create(self, payload):
        self.counter += 1
        rec = dict(payload)
        rec["id"] = str(self.counter)
        self.data.append(rec)
        return rec
    def update(self, payout_id, updates):
        for item in self.data:
            if str(item["id"]) == str(payout_id):
                item.update(updates)
                return item
        return None

def setup_repo(monkeypatch):
    repo = DummyRepo()
    monkeypatch.setattr(ar, "_repo", repo)
    return repo

def test_multiple_pending_requests_individual_update(monkeypatch):
    repo = setup_repo(monkeypatch)
    r1 = ar.log_new_request("u1", "A", "p", "b", 100, "m", "type")
    r2 = ar.log_new_request("u1", "A", "p", "b", 200, "m", "type")
    assert r1["id"] != r2["id"]
    assert repo.data[0]["status"] == "Ожидает"
    assert repo.data[1]["status"] == "Ожидает"
    ar.update_request_status(r1["id"], "approved")
    assert repo.data[0]["status"] == "Одобрено"
    assert repo.data[1]["status"] == "Ожидает"
    ar.update_request_status(r2["id"], "rejected")
    assert repo.data[1]["status"] == "Отклонено"
