from fastapi import APIRouter

from app.api.v1.bills import bills_router


v1_router = APIRouter(prefix="/v1")

v1_router.include_router(bills_router)