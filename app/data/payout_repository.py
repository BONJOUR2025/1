import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.config import ADVANCE_REQUESTS_FILE
from app.utils.logger import log


class PayoutRepository:
    def __init__(self, file_path: Optional[str] = None) -> None:
        self._file = file_path or ADVANCE_REQUESTS_FILE
        log(f"📂 Loading payouts from {self._file}")
        self._data: List[Dict[str, Any]] = self._load()
        log(f"✅ Loaded payouts: {len(self._data)}")
        if not self._data:
            log("⚠️ PayoutRepository loaded no payout records")
        self._counter = 0
        changed = False
        for item in self._data:
            raw_id = item.get("id")
            if raw_id is None or not str(raw_id).isdigit():
                self._counter += 1
                item["id"] = str(self._counter)
                changed = True
            else:
                self._counter = max(self._counter, int(raw_id))
        if changed:
            self._save()

    def _load(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self._file):
            example = self._file.replace(".json", ".example.json")
            if os.path.exists(example):
                log(f"⚠️ {self._file} not found. Using example {example}")
                try:
                    with open(example, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    with open(self._file, "w", encoding="utf-8") as out:
                        json.dump(data, out, ensure_ascii=False, indent=2)
                    return data
                except Exception as e:
                    log(f"❌ Failed reading example {example}: {e}")
                    return []
            log(f"❌ {self._file} not found and no example")
            return []
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            log(f"❌ Failed reading {self._file}: {e}")
            data = []
        if not data:
            example = self._file.replace(".json", ".example.json")
            if os.path.exists(example):
                try:
                    log(f"⚠️ Using example {example}")
                    with open(example, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    with open(self._file, "w", encoding="utf-8") as out:
                        json.dump(data, out, ensure_ascii=False, indent=2)
                except Exception as e:
                    log(f"❌ Failed reading example {example}: {e}")
                    data = []
        # normalize legacy status values
        status_map = {"В ожидании": "Ожидает", "Разрешено": "Одобрено"}
        changed = False
        for item in data:
            if item.get("status") in status_map:
                item["status"] = status_map[item["status"]]
                changed = True
        if changed:
            try:
                with open(self._file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as exc:
                log(f"❌ Failed to save normalized payouts: {exc}")
        return data

    def _save(self) -> None:
        with open(self._file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def _generate_id(self) -> str:
        self._counter += 1
        return str(self._counter)

    def load_all(self) -> List[Dict[str, Any]]:
        """Return raw payout list without filtering."""
        return list(self._data)

    def list(
        self,
        employee_id: Optional[str] = None,
        payout_type: Optional[str] = None,
        status: Optional[str] = None,
        method: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        result = []
        from_dt = datetime.fromisoformat(from_date) if from_date else None
        to_dt = datetime.fromisoformat(to_date) if to_date else None
        for item in self._data:
            if employee_id and str(item.get("user_id")) != str(employee_id):
                continue
            if payout_type and item.get("payout_type") != payout_type:
                continue
            if status and item.get("status") != status:
                continue
            if method and item.get("method") != method:
                continue
            ts_str = item.get("timestamp")
            created = None
            if ts_str:
                try:
                    created = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
            if from_dt and created and created < from_dt:
                continue
            if to_dt and created and created > to_dt:
                continue
            result.append(item)
        result.sort(key=lambda i: i.get("timestamp", ""), reverse=True)
        return result

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "id" not in data or any(
                p.get("id") == data["id"] for p in self._data):
            data["id"] = self._generate_id()
        self._data.append(data)
        self._save()
        return data

    def update(self, payout_id: str,
               updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for item in self._data:
            if str(item.get("id")) == str(payout_id):
                item.update(
                    {k: v for k, v in updates.items() if v is not None})
                self._save()
                return item
        return None

    def delete_many(self, ids: List[str]) -> None:
        self._data = [p for p in self._data if str(p.get("id")) not in ids]
        self._save()

    def delete(self, payout_id: str) -> bool:
        before = len(self._data)
        self._data = [
            p for p in self._data if str(
                p.get("id")) != str(payout_id)]
        if len(self._data) != before:
            self._save()
            return True
        return False
