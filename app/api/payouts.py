from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Optional

from app.schemas.payout import Payout, PayoutCreate, PayoutUpdate
from app.services.payout_service import PayoutService

__all__ = ["router", "init_payout_routes"]

router = APIRouter(tags=["Payouts"])


def init_payout_routes(service: PayoutService) -> None:

    @router.get("/", response_model=list[Payout])
    async def list_payouts(
        employee_id: Optional[str] = None,
        payout_type: Optional[str] = None,
        status: Optional[str] = None,
        method: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ):
        return await service.list_payouts(employee_id, payout_type, status, method, from_date, to_date)

    @router.post("/", response_model=Payout)
    async def create_payout(data: PayoutCreate):
        return await service.create_payout(data)

    @router.put("/{payout_id}", response_model=Payout)
    async def update_payout(payout_id: str, update: PayoutUpdate):
        updated = await service.update_payout(payout_id, update)
        if updated:
            return updated
        return Payout(
            id=payout_id,
            user_id="",
            name="",
            phone="",
            bank="",
            amount=0.0,
            method="",
            payout_type="",
            status="",
            timestamp=None)

    @router.put("/{payout_id}/status", response_model=Payout)
    async def set_status(payout_id: str, body: PayoutUpdate):
        if body.status is None:
            raise HTTPException(status_code=400, detail="status required")
        updated = await service.update_status(payout_id, body.status)
        if updated:
            return updated
        raise HTTPException(status_code=404, detail="not found")

    @router.delete("/{payout_id}")
    async def delete_payout(payout_id: str):
        deleted = await service.delete_payout(payout_id)
        if deleted:
            return {"detail": "deleted"}
        raise HTTPException(status_code=404, detail="not found")

    @router.get("/active", response_model=list[Payout])
    async def list_active_payouts():
        rows = await service.list_active_payouts()
        return rows

    @router.delete("/")
    async def delete_many(ids: str):
        id_list = [i for i in ids.split(",") if i]
        await service.delete_payouts(id_list)
        return {"ok": True}

    @router.get("/export.pdf")
    async def export_pdf(
        employee_id: Optional[str] = None,
        payout_type: Optional[str] = None,
        status: Optional[str] = None,
        method: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ):
        path = await service.export_to_pdf(
            employee_id, payout_type, status, method, from_date, to_date
        )
        if path:
            return FileResponse(Path(path), filename=Path(path).name)
        raise HTTPException(status_code=404, detail="No data")


