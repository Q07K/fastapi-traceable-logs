from typing import Any

from fastapi import APIRouter

from app.services.test import test_service_get, test_service_post

router = APIRouter(prefix="/test", tags=["test"])


@router.get(path="")
async def read_root() -> dict[str, Any]:
    result = await test_service_get()
    return {"result": result}


@router.post(path="")
async def create_item() -> dict[str, Any]:
    result = await test_service_post()
    return {"result": result}
